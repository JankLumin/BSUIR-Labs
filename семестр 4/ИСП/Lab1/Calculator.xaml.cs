namespace Lab1
{
    public partial class Calculator : ContentPage
    {
        private double currentNumber = 0;
        private double firstNumber = 0;
        private string currentOperation = null;
        private double secondNumber = 0;
        private string operation = "+";
        private bool check = false;
        public Calculator()
        {
            InitializeComponent();
        }
        private void OnDigitButtonClicked(object sender, EventArgs e)
        {
            Button clickedButton = (Button)sender;
            string digit = clickedButton.Text;
            this.result.Text += digit;
        }
        private void OnButtonClicked(object sender, EventArgs e)
        {
            Button clickedButton = (Button)sender;
            currentOperation = clickedButton.Text;
                switch (currentOperation)
                {
                    case "sin(x)":
                        if (double.TryParse(result.Text, out currentNumber))
                        {
                            currentNumber = Math.Sin(currentNumber * Math.PI / 180.0);
                            result.Text = currentNumber.ToString();
                        }
                        break;
                    case "C":
                        Clear();
                        break;
                    case "%":
                        if (double.TryParse(result.Text, out firstNumber))
                        {
                            check = true;
                            if (operation == "+" || operation == "-")
                            {
                                secondNumber = currentNumber / 100 * firstNumber;
                            }
                            else
                            {
                                secondNumber = firstNumber / 100;
                            }

                            Progress.Text = currentNumber + " " + operation + " " + secondNumber;
                            result.Text = secondNumber.ToString();
                        }
                        break;
                    case "del":
                        string text = result.Text;
                        if (!string.IsNullOrEmpty(text))
                        {
                            text = text.Substring(0, text.Length - 1);
                            result.Text = text;
                        }
                        break;
                    case "CE":
                        ClearEntry();
                        break;
                    case "+/-":
                        if (double.TryParse(result.Text, out currentNumber))
                        {
                            currentNumber = currentNumber * -1;
                            result.Text = currentNumber.ToString();
                        }
                        break;
                    case "1/x":
                        if (double.TryParse(result.Text, out currentNumber))
                        {
                            currentNumber = 1 / currentNumber;
                            result.Text = currentNumber.ToString();
                        }
                        break;
                    case "x^2":
                        if (double.TryParse(result.Text, out currentNumber))
                        {
                            currentNumber *= currentNumber;
                            result.Text = currentNumber.ToString();
                        }
                        break;
                    case "sqrt(x)":
                        if (double.TryParse(result.Text, out currentNumber))
                        {
                            currentNumber = Math.Sqrt(currentNumber);
                            result.Text = currentNumber.ToString();
                        }
                        break;
                    case "=":
                            HandleEquals();
                        break;
                    default:
                            HandleOperator();
                        break;
                }
        }
        private void ClearEntry()
        {
            result.Text = null;
            currentNumber = 0;
            operation = "+";
        }
        private void Clear()
        {
            operation = "+";
            currentNumber = 0;
            firstNumber = 0;
            currentOperation = null;
            secondNumber = 0;
            Progress.Text = null; 
            result.Text = null;
        }
        private void HandleOperator()
        {
            if (double.TryParse(result.Text, out secondNumber))
            {
                Calculate();
                operation = currentOperation;
                Progress.Text = currentNumber + " " + currentOperation;
                result.Text = null;
            }
        }

        private void HandleEquals()
        {
            if (check == false)
            {
                if (double.TryParse(result.Text, out secondNumber))
                {
                    Progress.Text = currentNumber + " " + operation + " " + secondNumber + " =";
                    Calculate();
                    result.Text = currentNumber.ToString();
                    operation = "";
                }
            }
            else
            {
                Progress.Text = currentNumber + " " + operation + " " + secondNumber + " =";
                Calculate();
                result.Text = currentNumber.ToString();
                operation = "";
            }
        }

        private void Calculate()
        {
            switch (operation)
            {
                case "+":
                    currentNumber += secondNumber;
                    break;
                case "-":
                    currentNumber -= secondNumber;
                    break;
                case "*":
                    currentNumber *= secondNumber;
                    break;
                case "/":
                    if (secondNumber != 0)
                        currentNumber /= secondNumber;
                    else
                        result.Text = "Error";
                    break;
            }
        }
    }
}
