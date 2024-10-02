using Microsoft.AspNetCore.Mvc.TagHelpers;
using Microsoft.AspNetCore.Razor.TagHelpers;
using Microsoft.AspNetCore.Routing;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc.Rendering;

namespace WEB_253504_Frolenko.UI.TagHelpers
{
    [HtmlTargetElement("pager")]
    public class PagerTagHelper : TagHelper
    {
        private readonly LinkGenerator _linkGenerator;
        private readonly IHttpContextAccessor _httpContextAccessor;

        public PagerTagHelper(LinkGenerator linkGenerator, IHttpContextAccessor httpContextAccessor)
        {
            _linkGenerator = linkGenerator;
            _httpContextAccessor = httpContextAccessor;
        }

        [HtmlAttributeName("current-page")]
        public int CurrentPage { get; set; }

        [HtmlAttributeName("total-pages")]
        public int TotalPages { get; set; }

        [HtmlAttributeName("category")]
        public string? Category { get; set; }

        [HtmlAttributeName("admin")]
        public bool Admin { get; set; } = false;

        public override void Process(TagHelperContext context, TagHelperOutput output)
        {
            output.TagName = "ul";
            output.Attributes.Add("class", "pagination justify-content-center");

            if (CurrentPage > 1)
            {
                output.Content.AppendHtml(CreatePageItem(CurrentPage - 1, "Предыдущая"));
            }

            for (int i = 1; i <= TotalPages; i++)
            {
                output.Content.AppendHtml(CreatePageItem(i, i.ToString()));
            }

            if (CurrentPage < TotalPages)
            {
                output.Content.AppendHtml(CreatePageItem(CurrentPage + 1, "Следующая"));
            }
        }

        private TagBuilder CreatePageItem(int page, string text)
        {
            var li = new TagBuilder("li");
            li.AddCssClass("page-item");
            if (page == CurrentPage)
            {
                li.AddCssClass("active");
            }

            var a = new TagBuilder("a");
            a.AddCssClass("page-link");
            a.Attributes["href"] = GeneratePageLink(page);
            a.InnerHtml.Append(text);

            li.InnerHtml.AppendHtml(a);
            return li;
        }

        private string GeneratePageLink(int page)
        {
            var httpContext = _httpContextAccessor.HttpContext;
            if (httpContext == null)
            {
                throw new InvalidOperationException("HttpContext is null.");
            }

            string? url = null;

            if (Admin)
            {
                var values = new RouteValueDictionary
                {
                    { "pageNo", page }
                };

                url = _linkGenerator.GetPathByPage(
                    page: "/Admin/Index",
                    values: values,
                    pathBase: httpContext.Request.PathBase);
            }
            else
            {
                var values = new RouteValueDictionary
                {
                    { "pageNo", page }
                };

                if (!string.IsNullOrEmpty(Category))
                {
                    values["category"] = Category;
                }

                url = _linkGenerator.GetPathByAction(
                    action: "Index",
                    controller: "Product",
                    values: values,
                    httpContext: httpContext);
            }

            return url ?? "#";
        }
    }
}
