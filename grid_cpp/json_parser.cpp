#include "json_parser.h"

// Function to trim leading and trailing whitespace and quotes
std::string trim_string(const std::string &str)
{
    size_t first = str.find_first_not_of(" \t\n\r\"");
    size_t last = str.find_last_not_of(" \t\n\r\"");
    if (first == std::string::npos || last == std::string::npos)
    {
        return "";  // Return empty string if all characters are whitespace or quotes
    }
    return str.substr(first, last - first + 1);
}

void extract_rules(const std::string &content, std::vector<std::vector<std::string>> &rules)
{
    std::string::size_type start = content.find("\"base_of_rules\": [");
    if (start == std::string::npos)
        return;

    start += 18; // Skip past the key and opening bracket
    std::string::size_type end = content.find("]", start);
    std::string rulesSection = content.substr(start, end - start);

    std::istringstream ss(rulesSection);
    std::string ruleStr;
    while (std::getline(ss, ruleStr, ','))
    {
        // Trim the entire rule string
        ruleStr = trim_string(ruleStr);

        // Find the delimiter '=>'
        std::string::size_type pos = ruleStr.find("=>");
        if (pos != std::string::npos)
        {
            std::string body = trim_string(ruleStr.substr(0, pos));
            std::string head = trim_string(ruleStr.substr(pos + 2));

            rules.push_back({body, head});
        }
    }
}

void extract_facts_base(const std::string &content, std::vector<std::string> &factsBase)
{
    std::string::size_type start = content.find("\"base_of_facts\": [");
    if (start == std::string::npos)
        return;

    start += 18; // Skip past the key and opening bracket
    std::string::size_type end = content.find("]", start);
    std::string factsSection = content.substr(start, end - start);

    std::istringstream ss(factsSection);
    std::string fact;
    while (std::getline(ss, fact, ','))
    {
        // Trim the entire fact string
        fact = trim_string(fact);

        if (!fact.empty())
        {
            factsBase.push_back(fact);
        }
    }
}

std::string extract_question(const std::string &content)
{
    std::string::size_type start = content.find("\"question\": \"");
    if (start == std::string::npos)
        return "";

    start += 13; // Skip past the key and opening quote
    std::string::size_type end = content.find("\"", start);
    return content.substr(start, end - start);
}


std::unordered_map<std::string, std::shared_ptr<std::any>> parse_json(const std::string &filename)
{
    std::unordered_map<std::string, std::shared_ptr<std::any>> data;

     // Prepend the folder path to the filename
    std::string filePath = "../json_andor/" + filename;

    std::ifstream inputFile(filePath);
    if (!inputFile.is_open())
    {
        std::cerr << "Could not open the file: " << filename << std::endl;
        return data;
    }

    std::ostringstream oss;
    oss << inputFile.rdbuf();
    std::string content = oss.str();
    inputFile.close();

    // Extract rules
    std::vector<std::vector<std::string>> rules;
    extract_rules(content, rules);
    data["rules"] = std::make_shared<std::any>(rules);

    // Extract facts
    std::vector<std::string> factsBase;
    extract_facts_base(content, factsBase);
    data["facts base"] = std::make_shared<std::any>(factsBase);

    // Extract question
    std::string question = extract_question(content);
    data["question"] = std::make_shared<std::any>(question);

    return data;
}



