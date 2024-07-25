using System.Collections.ObjectModel;
using Lab1.Services;
using Lab1.Entities;

namespace Lab1
{
    public partial class SQL : ContentPage
    {
        private IDbService sqliteService;
        public ObservableCollection<Brand> Brands { get; set; }
       
        public SQL(IDbService dbService)
        {
            InitializeComponent();
            
            sqliteService = dbService;
            sqliteService.Init();
            
        }

        private void LoadBrands(object sender, EventArgs e)
        {
            Brands = new ObservableCollection<Brand>(sqliteService.GetAllBrands());
            brandPicker.ItemsSource = Brands;
        }

        private void OnBrandSelected(object sender, EventArgs e)
        {
            var selectedBrand = (Brand)brandPicker.SelectedItem;
            if (selectedBrand != null)
            {
                var products = sqliteService.GetBrandProducts(selectedBrand.Id);
                productCollectionView.ItemsSource = products;
            }
        }
    }
}