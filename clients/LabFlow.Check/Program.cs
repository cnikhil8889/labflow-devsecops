// CNK | Nikhil Kumar Choudavarapu | LabFlow DevSecOps
using System.Text.Json;
using var client = new HttpClient { Timeout = TimeSpan.FromSeconds(5) };
var endpoint = Environment.GetEnvironmentVariable("LABFLOW_URL") ?? "http://127.0.0.1:8080";
var uri = new Uri(endpoint);
if (!uri.IsLoopback || uri.Scheme != "http") throw new ArgumentException("Use a loopback HTTP port-forward");
using var response = await client.GetAsync(new Uri(uri, "/healthz"));
response.EnsureSuccessStatusCode();
using var document = JsonDocument.Parse(await response.Content.ReadAsStringAsync());
if (document.RootElement.GetProperty("status").GetString() != "ok") throw new InvalidOperationException("Unhealthy service");
Console.WriteLine("CNK | LabFlow health check passed");
