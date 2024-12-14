#include "stm32_app.h"
#include "tensorflow/lite/experimental/micro/kernels/all_ops_resolver.h"
#include "tensorflow/lite/experimental/micro/micro_error_reporter.h"
#include "tensorflow/lite/experimental/micro/micro_interpreter.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "tensorflow/lite/version.h"
#include "model.h"
#include "mnist.h"

#include <cstdlib>
#include <ctime>
#include <algorithm>
#include <cstring>

constexpr int kTensorArenaSize = 16000;
constexpr int kImageWidth = 28;
constexpr int kImageHeight = 28;

const tflite::Model *model = nullptr;
tflite::MicroInterpreter *interpreter = nullptr;
tflite::ErrorReporter *reporter = nullptr;
TfLiteTensor *input = nullptr;
TfLiteTensor *output = nullptr;
uint8_t tensor_arena[kTensorArenaSize] = {0};
float *input_buffer = nullptr;

const char *class_mapping[] = {
    "A", "a", "B", "b", "V", "v", "G", "g", "D", "d",
    "E", "e", "Yo", "yo", "Zh", "zh", "Z", "z", "I", "i",
    "J", "K", "k", "L", "l", "M", "m", "N", "n", "O", "o",
    nullptr, nullptr, "P", "p", "R", "r", "S", "s", "T", "t",
    "U", "u", nullptr, nullptr, "F", "f", "H", "h", "C", "c",
    "Ch", "ch", "Sh", "sh", "Shch", "shch", "HardSign", "Yi", "SoftSign", "Eh", "eh",
    "Yu", "yu", "Ya", "ya",
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"};

void CheckPointer(void *ptr, const char *error_message)
{
    if (ptr == nullptr)
    {
        if (reporter)
        {
            reporter->Report(error_message);
        }
        while (true)
        {
        }
    }
}

void bitmap_to_float_array(float *dest, const unsigned char *bitmap)
{
    int pixel = 0;
    int bytes_per_row = (kImageWidth + 7) / 8;
    for (int y = 0; y < kImageHeight; y++)
    {
        for (int x = 0; x < kImageWidth; x++)
        {
            int byte_index = x / 8;
            int bit_index = x % 8;
            dest[pixel] = (bitmap[y * bytes_per_row + byte_index] >> (7 - bit_index)) & 0x1 ? 1.0f : 0.0f;
            pixel++;
        }
    }
}

void draw_input_buffer()
{
    CheckPointer(input_buffer, "Input buffer is nullptr in draw_input_buffer");

    clear_display();
    for (int y = 0; y < kImageHeight; y++)
    {
        for (int x = 0; x < kImageWidth; x++)
        {
            draw_pixel(x + 16, y + 3, input_buffer[y * kImageWidth + x] > 0 ? 0xFFFFFFFF : 0xFF000000);
        }
    }
}

void setup()
{
    srand(static_cast<unsigned int>(time(nullptr)));

    static tflite::MicroErrorReporter error_reporter_instance;
    reporter = &error_reporter_instance;
    CheckPointer(reporter, "Failed to initialize error reporter");
    reporter->Report("Initializing model...");

    model = tflite::GetModel(tf_model);
    CheckPointer((void *)model, "Failed to load model");

    if (model->version() != TFLITE_SCHEMA_VERSION)
    {
        reporter->Report("Model schema mismatch. Expected %d but got %d", TFLITE_SCHEMA_VERSION, model->version());
        while (true)
            ;
    }

    static tflite::ops::micro::AllOpsResolver resolver;
    static tflite::MicroInterpreter static_interpreter(model, resolver, tensor_arena, kTensorArenaSize, reporter);
    interpreter = &static_interpreter;
    CheckPointer(interpreter, "Failed to initialize interpreter");

    if (interpreter->AllocateTensors() != kTfLiteOk)
    {
        reporter->Report("Failed to allocate tensors");
        while (true)
            ;
    }

    input = interpreter->input(0);
    CheckPointer(input, "Input tensor is nullptr");

    output = interpreter->output(0);
    CheckPointer(output, "Output tensor is nullptr");

    input_buffer = input->data.f;
    CheckPointer(input_buffer, "Input buffer is nullptr after assignment");
}

void loop()
{
    const int num_test_images = (sizeof(test_images) / sizeof(test_images[0]));

    if (num_test_images == 0)
    {
        reporter->Report("No test images found.");
        while (true)
            ;
    }

    int random_index = rand() % num_test_images;
    bitmap_to_float_array(input_buffer, test_images[random_index]);
    draw_input_buffer();

    if (interpreter->Invoke() != kTfLiteOk)
    {
        reporter->Report("Invoke failed");
        while (true)
            ;
    }

    CheckPointer(output, "Output tensor is nullptr before accessing data.f");

    float *result = output->data.f;
    CheckPointer(result, "Output data.f is nullptr");

    CheckPointer(output->dims, "Output dims is nullptr");
    CheckPointer(output->dims->data, "Output dims data is nullptr");

    int output_size = output->dims->data[1];
    int predicted_class = std::distance(result, std::max_element(result, result + output_size));

    const char *predicted_label = nullptr;
    if (predicted_class >= 0 && predicted_class < static_cast<int>(sizeof(class_mapping) / sizeof(class_mapping[0])))
    {
        predicted_label = class_mapping[predicted_class];
    }

    char resultText[256];
    if (predicted_label != nullptr)
    {
        snprintf(resultText, sizeof(resultText), "It looks like a: %s", predicted_label ? predicted_label : "unknown");
    }
    else
    {
        snprintf(resultText, sizeof(resultText), "Failed to recognize");
    }

    draw_text(resultText, 0xFF0000FF);
    delay(1000);
}
