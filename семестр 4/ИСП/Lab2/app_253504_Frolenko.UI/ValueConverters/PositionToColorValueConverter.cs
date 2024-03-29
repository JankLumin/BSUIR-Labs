using System.Globalization;
namespace app_253504_Frolenko.UI.ValueConverters;
internal class PositionToColorValueConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
    {
        if ((int)value < 6)
            return Colors.LightPink;
        return Colors.PapayaWhip;
    }
    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
    {
        throw new NotImplementedException();
    }
}