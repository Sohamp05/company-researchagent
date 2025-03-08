import React, { useState } from "react";
import { Search, Building2, Globe, Loader2 } from "lucide-react";
import { parse } from "yaml";

interface CompanyData {
  name?: string;
  website?: string;
  description?: string;
  founded?: string;
  headquarters?: string;
  employees?: string;
  industry?: string;
  products?: string[];
  competitors?: string[];
  revenue?: string;
  [key: string]: any;
}

function App() {
  const [input, setInput] = useState(""); // To store the company name input
  const [isLoading, setIsLoading] = useState(false); // To handle loading state
  const [error, setError] = useState(""); // To handle error messages
  const [companyData, setCompanyData] = useState<CompanyData | null>(null); // To store the company data fetched from backend

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(""); // Reset error message

    try {
      // Make the API call to the Flask backend with the company name
      const response = await fetch(
        `http://localhost:5000/agent?company=${input}`
      );

      if (!response.ok) {
        throw new Error("Failed to fetch data");
      }

      // Get the response text (YAML data) and parse it
      const yamlResponse = await response.text();
      const parsedData = parse(yamlResponse); // Convert YAML into JSON
      setCompanyData(parsedData); // Set the parsed data into the state
    } catch (err) {
      setError("Failed to fetch company data. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-4">
            <Building2 className="h-12 w-12 text-indigo-600" />
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Company Research Assistant
          </h1>
          <p className="text-lg text-gray-600">
            Enter a company name to get detailed insights
          </p>
        </div>

        {/* Company name input and submit button */}
        <form onSubmit={handleSubmit} className="mb-8">
          <div className="relative">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)} // Update the company name on input change
              placeholder="Enter company name (e.g., Zomato)"
              className="w-full px-6 py-4 text-lg border-2 border-gray-200 rounded-lg focus:outline-none focus:border-indigo-500 pr-12"
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()} // Disable the button when loading or input is empty
              className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <Loader2 className="h-6 w-6 animate-spin" />
              ) : (
                <Search className="h-6 w-6" />
              )}
            </button>
          </div>
        </form>

        {/* Display error message if any */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-8">
            <p className="text-red-700">{error}</p>
          </div>
        )}

        {/* Display company data if successfully fetched */}
        {companyData && (
          <div className="bg-white rounded-xl shadow-lg p-6 animate-fade-in">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">
                {companyData.name || "Company Name"}
              </h2>
              {companyData.website && (
                <a
                  href={`https://${companyData.website}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center text-indigo-600 hover:text-indigo-800"
                >
                  <Globe className="h-5 w-5 mr-2" />
                  {companyData.website}
                </a>
              )}
            </div>

            {/* Display detailed company information */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div>
                  <h3 className="text-sm font-semibold text-gray-500 uppercase">
                    Description
                  </h3>
                  <p className="mt-1 text-gray-900">
                    {companyData.description}
                  </p>
                </div>

                <div>
                  <h3 className="text-sm font-semibold text-gray-500 uppercase">
                    Founded
                  </h3>
                  <p className="mt-1 text-gray-900">{companyData.founded}</p>
                </div>

                <div>
                  <h3 className="text-sm font-semibold text-gray-500 uppercase">
                    Headquarters
                  </h3>
                  <p className="mt-1 text-gray-900">
                    {companyData.headquarters}
                  </p>
                </div>

                <div>
                  <h3 className="text-sm font-semibold text-gray-500 uppercase">
                    Employees
                  </h3>
                  <p className="mt-1 text-gray-900">{companyData.employees}</p>
                </div>
              </div>

              <div className="space-y-4">
                <div>
                  <h3 className="text-sm font-semibold text-gray-500 uppercase">
                    Industry
                  </h3>
                  <p className="mt-1 text-gray-900">{companyData.industry}</p>
                </div>

                <div>
                  <h3 className="text-sm font-semibold text-gray-500 uppercase">
                    Products
                  </h3>
                  <ul className="mt-1 list-disc list-inside text-gray-900">
                    {companyData.products?.map((product, index) => (
                      <li key={index}>{product}</li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h3 className="text-sm font-semibold text-gray-500 uppercase">
                    Competitors
                  </h3>
                  <ul className="mt-1 list-disc list-inside text-gray-900">
                    {companyData.competitors?.map((competitor, index) => (
                      <li key={index}>{competitor}</li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h3 className="text-sm font-semibold text-gray-500 uppercase">
                    Revenue
                  </h3>
                  <p className="mt-1 text-gray-900">{companyData.revenue}</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
