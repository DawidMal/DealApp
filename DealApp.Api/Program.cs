using System.Net;
using System.Net.Http.Headers;
using HtmlAgilityPack;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddHttpClient();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.MapGet("/search", async (string q, IHttpClientFactory httpClientFactory, CancellationToken cancellationToken) =>
{
    if (string.IsNullOrWhiteSpace(q))
    {
        return Results.BadRequest(new { error = "Query parameter 'q' is required." });
    }

    var httpClient = httpClientFactory.CreateClient();
    httpClient.DefaultRequestHeaders.UserAgent.Add(new ProductInfoHeaderValue("DealApp", "1.0"));
    httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("text/html"));

    var encodedQuery = Uri.EscapeDataString(q);
    var requestUrl = $"https://www.takealot.com/all?_sb=1&_r=1&_si=9ede1d4c09a3f19b0bcf8d9487e37477&qsearch={encodedQuery}";

    using var response = await httpClient.GetAsync(requestUrl, cancellationToken);

    if (!response.IsSuccessStatusCode)
    {
        return Results.Problem(title: "Unable to fetch search results.", statusCode: (int)response.StatusCode);
    }

    var html = await response.Content.ReadAsStringAsync(cancellationToken);
    var document = new HtmlDocument();
    document.LoadHtml(html);

    var productCards = document.DocumentNode.SelectNodes("//div[contains(@class,'product-card')]");

    var products = productCards?
        .Select(card =>
        {
            var linkNode = card.SelectSingleNode(".//a[contains(@class,'product-card')]");
            var titleNode = card.SelectSingleNode(".//span[contains(@class,'title')] | .//div[contains(@class,'product-title')]//span");
            var priceNode = card.SelectSingleNode(".//span[contains(@class,'currency')] | .//span[contains(@class,'price')]//span[contains(@class,'amount')]" );

            var link = linkNode?.GetAttributeValue("href", string.Empty) ?? string.Empty;
            if (!string.IsNullOrEmpty(link) && link.StartsWith("/"))
            {
                link = $"https://www.takealot.com{link}";
            }

            var title = titleNode?.InnerText?.Trim() ?? string.Empty;
            var price = priceNode?.InnerText?.Trim() ?? string.Empty;

            return new ProductResult(
                Title: WebUtility.HtmlDecode(title),
                Price: WebUtility.HtmlDecode(price),
                Link: link);
        })
        .Where(product => !string.IsNullOrEmpty(product.Title) && !string.IsNullOrEmpty(product.Link))
        .Take(5)
        .ToList() ?? new List<ProductResult>();

    return Results.Ok(products);
})
.WithName("SearchProducts")
.WithOpenApi();

app.Run();

record ProductResult(string Title, string Price, string Link);
