#include <iostream>
#include <string>
#include <stdexcept>
#include <ghc/filesystem.hpp>

#define MP3_ID3_TAGS_USE_GENRES
#define MP3_ID3_TAGS_IMPLEMENTATION
#include "mp3_id3_tags.h"

namespace fs = ghc::filesystem;

mp3_id3_tags parseFile(const char* fileName) {  // т.к. библиотека mp3_id3_tags написана на Си, то и функция parseFile в Си стиле
    FILE *f = fopen(fileName, "rb");

    mp3_id3_tags tags;
    if (f) {
        if (mp3_id3_file_read_tags(f, &tags)) {
            
        } else {
            std::cout << (std::string("error: ") + mp3_id3_failure_reason());
        }

        fclose(f);
    } else {
        std::cout << (std::string("failed to open/read file ") + fileName);
    }

    return tags;
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        // printf("использование: %s \"Название файла\" или \"Название папки\"\n", argv[0]);
        printf("using: %s \"directory name\" \"output file name\"\n", argv[0]);
        return 0;
    }
    
    std::string path = std::string(argv[1]);
    std::string JSONstr = "[\n";
    auto dirIterator = fs::directory_iterator(path);
    for (const auto & entry : dirIterator) {
        std::string filePath = entry.path().string();
        const char* filePathChar = filePath.c_str();
        std::cout << "file: " << filePathChar << std::endl;
        mp3_id3_tags useless;
        bool isError = !mp3_id3_file_read_tags(fopen(filePathChar, "rb"), &useless);
        if (isError) {
            std::cout << "ERROR in " << filePathChar << std::endl;
            continue;
        }
        mp3_id3_tags tags = parseFile(filePathChar);
        
        if (JSONstr != "[\n")
            JSONstr += ",\n";
        JSONstr += "\t{\n";
        JSONstr += "\t\t" + std::string("\"File\": \"") + filePathChar + "\",\n";
        JSONstr += "\t\t" + std::string("\"Title\": \"") + tags.title + "\",\n";
        JSONstr += "\t\t" + std::string("\"Artist\": \"") + tags.artist + "\",\n";
        JSONstr += "\t\t" + std::string("\"Album\": \"") + tags.album + "\",\n";
        JSONstr += "\t\t" + std::string("\"Year\": \"") + tags.year + "\",\n";
        JSONstr += "\t\t" + std::string("\"Comment\": \"") + tags.comment + "\",\n";
        JSONstr += "\t\t" + std::string("\"Genre\": \"") + tags.genre + "\",\n";
        JSONstr += "\t}";
    }
    JSONstr += "\n]";
    
    std::ofstream outfile(argv[2]);
    outfile << JSONstr << std::endl;
    outfile.close();
    std::cout << "successfully created!" << std::endl;
}