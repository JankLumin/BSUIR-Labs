using System;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Maui.Controls;

namespace Lab1
{
    public partial class Integral : ContentPage
    {
        private CancellationTokenSource Token;

        public Integral()
        {
            InitializeComponent();
        }

        private async void StartButton_Clicked(object sender, EventArgs e)
        {
            Token?.Cancel();
            Token = new CancellationTokenSource();
            try
            {
                StatusLabel.Text = "Вычисление ";
                ProgressLabel.Text = "0%";
                double result = await Task.Run(() => CalculateIntegralAsync(Token.Token));

                StatusLabel.Text = $"Результат: {result:F5}";
                ProgressLabel.Text = "100%";
            }
            catch (OperationCanceledException)
            {
                StatusLabel.Text = "Задание отменено";
            }
        }
        private async Task<double> CalculateIntegralAsync(CancellationToken cancellationToken)
        {
            double a = 0;
            double b = 1;
           // double step = 0.00000001;
            double step = 0.0001;
            double progress;
            double result = 0;
            int iterations = 100000;

            for (double x = a; x < b; x += step)
            {
                cancellationToken.ThrowIfCancellationRequested();

                result += Math.Sin(x) * step;
                progress = (x - a) / (b - a) * 100;
                
                Device.BeginInvokeOnMainThread(() => ProgressLabel.Text = $"{progress:F5}%");
                
                ProgressBar.Progress = progress / 100;
                
                await Task.Delay(1, cancellationToken);
            }

            return result;
        }
        private void CancelButton_Clicked(object sender, EventArgs e)
        {
            Token?.Cancel();
        }
    }
}
