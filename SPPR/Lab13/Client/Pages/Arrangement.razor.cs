using global::System.Collections.Generic;
using global::System.Linq;
using global::System.Threading.Tasks;
using System.Net.Http;
using System.Net.Http.Json;
using Microsoft.AspNetCore.Components.Forms;
using Microsoft.AspNetCore.Components.Routing;
using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.Web.Virtualization;
using Microsoft.AspNetCore.Components.WebAssembly.Http;
using Microsoft.JSInterop;
using Client;
using Client.Layout;
using Client.Services;
using Share.Models;
using Microsoft.AspNetCore.WebUtilities;
using Newtonsoft.Json;
using Microsoft.AspNetCore.Components;
using System.Drawing;

namespace Client.Pages
{
    public partial class Arrangement : IDisposable
    {
        [Inject] private IJSRuntime _jsRuntime { get; init; } = null!;
        [Inject] private NavigationManager _navigationManager { get; init; } = null!;
        [Inject] private IPageJsInvokeService _pageJsInvokeService { get; init; } = null!;
        [Inject] private IGameService _gameService { get; init; } = null!;
        [SupplyParameterFromQuery]
        [Parameter]
        public string GameId { get; set; } = "";
        [SupplyParameterFromQuery]
        [Parameter]
        public string Username { get; set; } = "";
        private IDisposable? _wait;
        private IDisposable? _start;
        private int[,]? field = new int[10, 10];
        private GridBuilder _gridBuilder;
        private bool _disposed = false;

        public Arrangement()
        {
            _gridBuilder = new GridBuilder();
        }

        [JSInvokable]
        public Task AddShip(int x, int y, int size, Orientation orientation)
        {
            _gridBuilder.AddShip(new Ship(x, y, size, orientation));
            _gridBuilder.SaveSelectedShip();
            return Task.CompletedTask;
        }

        [JSInvokable]
        public Task RemoveShip(int x, int y)
        {
            _gridBuilder.SelectShip(x, y);
            _gridBuilder.RemoveSelectedShip();
            return Task.CompletedTask;
        }

        [JSInvokable]
        public Task ClearShips()
        {
            _gridBuilder.Clear();
            return Task.CompletedTask;
        }

        protected async override Task OnInitializedAsync()
        {
            _start = _gameService.CreateConnection("Start", () =>
            {
                _navigationManager.NavigateTo($"/play?GameId={GameId}&Username={Username}");
            });
            _wait = _gameService.CreateConnection("Wait", () =>
            {
                _navigationManager.NavigateTo($"/waiting?GameId={GameId}&Username={Username}");
            });

            await _gameService.ConnectToHub();
        }

        private async Task UpdateFieldAsync()
        {
            int[] preField = await _jsRuntime.InvokeAsync<int[]>("getMatrix");

            for (int i = 0; i < 10; i++)
            {
                for (int j = 0; j < 10; j++)
                {
                    int index = i * 10 + j;
                    field![i, j] = preField[index];
                }
            }
        }

        private async Task InitializeScript()
        {
            await _jsRuntime.InvokeVoidAsync("Init");
        }

        protected override async Task OnAfterRenderAsync(bool firstRender)
        {
            if (firstRender)
            {
                await InitializeScript();

                await _pageJsInvokeService.RegisterAsync(this);
            }

            await base.OnAfterRenderAsync(firstRender);
        }

        private async Task Ready()
        {
            await UpdateFieldAsync();

            string serializedField = JsonConvert.SerializeObject(field);
            var divContent = await _jsRuntime.InvokeAsync<string>("getDivContent", "field");

            await _gameService.AddContent(Username, divContent);
            await _gameService.AddMove(GameId, Username);

            await _gameService.StartGame(GameId, Username, serializedField);
        }

        public void Dispose()
        {
            if (_disposed)
                return;

            _wait?.Dispose();
            _start?.Dispose();

            _pageJsInvokeService.UnregisterAsync<Arrangement>();

            _disposed = true;
            GC.SuppressFinalize(this);
        }
    }
}