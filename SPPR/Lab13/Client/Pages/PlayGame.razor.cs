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
using System;
using System.Collections.Specialized;
using System.Web;

namespace Client.Pages
{

    public partial class PlayGame
    {
        [SupplyParameterFromQuery]
        [Parameter]
        public string GameId { get; set; } = "";
        [SupplyParameterFromQuery]
        [Parameter]
        public string Username { get; set; } = "";
        private string matrix = "";
        private string content = "";
        private bool move = false;
        private readonly List<MarkupString> iconHtmlList = new();
        private readonly List<MarkupString> getIconHtmlList = new();
        private IDisposable? _change;
        private IDisposable? _finish;
        private IDisposable? _getMove;

        protected async override Task OnInitializedAsync()
        {
            content = await GameService.GetContent(Username!);
            move = (await GameService.GetMove(GameId!)) == Username;
            _getMove = GameService.CreateConnection("GetMove", async (x, y, shot) =>
            {
                string iconHtml = await JSRuntime.InvokeAsync<string>(shot ? "getshot" : "getmiss", x, y);
                getIconHtmlList.Add(new MarkupString(iconHtml));
                StateHasChanged();
            });
            _change = GameService.CreateConnection("Change", () =>
            {
                move = !move;
                StateHasChanged();
            });
            _finish = GameService.CreateConnection("Finish", (username) =>
            {
                NavigationManager.NavigateTo($"/results?GameId={GameId}&Username={username}");
                StateHasChanged();
            });

            await GameService.ConnectToHub();
            matrix = await GameService.GetOpponentField(GameId, Username);
            await JSRuntime.InvokeVoidAsync("GameInit", matrix);
            StateHasChanged();
        }

        private async Task Click(MouseEventArgs e)
        {
            string iconHtml = await JSRuntime.InvokeAsync<string>("onOtherField", e);

            iconHtmlList.Add(new MarkupString(iconHtml));
            StateHasChanged();
            string innerText = await JSRuntime.InvokeAsync<string>("getResults");

            if (innerText == "Victory")
            {
                await GameService.EndGame(GameId, Username);
                StateHasChanged();
                return;
            }
            else if (innerText == "Skip")
            {
                return;
            }

            string[] parts = innerText.Split(' ');
            try
            {
                int.TryParse(parts[0], out int x);
                int.TryParse(parts[1], out int y);
                bool.TryParse(parts[2], out bool shot);

                await GameService.Move(GameId, Username, x, y, shot);
                StateHasChanged();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Ошибка: {ex.Message}");
            }
        }

        public void Dispose()
        {
            _change?.Dispose();
            _finish?.Dispose();
            _getMove?.Dispose();
        }
    }
}