namespace WEB_253504_Frolenko.UI.Services.FileService
{
    public class ApiFileService : IFileService
    {
        private readonly HttpClient _httpClient;

        public ApiFileService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<string> SaveFileAsync(IFormFile formFile)
        {
            if (formFile == null)
            {
                Console.WriteLine("Ошибка: файл не передан.");
                throw new ArgumentNullException(nameof(formFile));
            }

            Console.WriteLine($"Начинаем загрузку файла: {formFile.FileName}");

            var request = new HttpRequestMessage(HttpMethod.Post, "files");

            var extension = Path.GetExtension(formFile.FileName);
            var newName = Path.ChangeExtension(Path.GetRandomFileName(), extension);
            Console.WriteLine($"Формируем новое имя файла: {newName}");

            var content = new MultipartFormDataContent();
            var streamContent = new StreamContent(formFile.OpenReadStream());
            content.Add(streamContent, "file", newName);
            Console.WriteLine("Контент для отправки сформирован.");

            request.Content = content;

            Console.WriteLine("Отправляем запрос на сервер...");
            var response = await _httpClient.SendAsync(request);

            if (response.IsSuccessStatusCode)
            {
                var responseContent = await response.Content.ReadAsStringAsync();
                Console.WriteLine($"Файл успешно загружен. URL: {responseContent}");
                return responseContent;
            }
            else
            {
                Console.WriteLine($"Ошибка при загрузке файла: {response.StatusCode}");
                throw new InvalidOperationException($"Ошибка при загрузке файла: {response.StatusCode}");
            }
        }

        public async Task DeleteFileAsync(string fileUri)
        {
            if (string.IsNullOrEmpty(fileUri))
            {
                Console.WriteLine("Ошибка: URI файла для удаления не передан.");
                throw new ArgumentNullException(nameof(fileUri));
            }

            Console.WriteLine($"Начинаем удаление файла по URI: {fileUri}");

            var response = await _httpClient.DeleteAsync(fileUri);

            if (response.IsSuccessStatusCode)
            {
                Console.WriteLine("Файл успешно удалён.");
            }
            else
            {
                Console.WriteLine($"Ошибка при удалении файла: {response.StatusCode}");
                throw new InvalidOperationException($"Ошибка при удалении файла: {response.StatusCode}");
            }
        }
    }
}
