from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
import os
import sys

# Эта функция завайбкодена
def get_audio_info(file_path):
    if not os.path.exists(file_path):
        raise Exception("Файл " + file_path + " не найден")

    artist = "Неизвестный исполнитель"
    title = "Без названия"
    file_type = "Не определен"

    try:
        # Шаг 1: Пробуем открыть как настоящий MP3
        audio = MP3(file_path)
        file_type = "Настоящий MP3"

        # Безопасно проверяем, есть ли теги вообще
        if audio.tags is not None:
            # В MP3 теги называются TPE1 (исполнитель) и TIT2 (название)
            artist = str(audio.tags.get("TPE1", artist))
            title = str(audio.tags.get("TIT2", title))
            # Проверяем, есть ли признаки сломанной кодировки (символы из Latin-1)
            # Если в строке есть специфичные символы вроде 'Ñ', 'å', 'ì', пробуем починить
            if any(char in title for char in "ÑåìîòÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ"):
                # Откатываем строку назад в байты ISO-8859-1 и декодируем в правильный Windows-1251
                title = title.encode('iso-8859-1').decode('cp1251')
        else:
            artist += " (теги пусты)"

    except Exception:
        # Шаг 2: Если MP3 ругается на заголовок, пробуем открыть как MP4 (видео контейнер)
        try:
            audio = MP4(file_path)
            file_type = "Замаскированный MP4"

            if audio.tags is not None:
                # В MP4 теги хранятся под другими именами
                artist_list = audio.tags.get("\xa9ART")
                title_list = audio.tags.get("\xa9nam")

                if artist_list:
                    artist = artist_list[0]
                if title_list:
                    title = title_list[0]
            else:
                artist += " (теги пусты)"
        except Exception as e:
            return f"Ошибка: файл поврежден или это другой формат. ({e})"

    # Получаем длительность (она доступна и в MP3, и в MP4)
    duration = f"{audio.info.length:.2f} сек" if audio.info else "Н/Д"

    return {
        "Тип": file_type,
        "Исполнитель": artist,
        "Название": title,
        "Длительность": duration,
    }


if __name__ == '__main__':
    directory = sys.argv[1]
    fileNames = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    fileNames.sort()

    outputFileName = sys.argv[2]
    with open(outputFileName, "w", encoding="utf-8") as f:
        lines = []
        for fileName in fileNames:
            filePath = directory + "\\" + fileName
            data = get_audio_info(filePath)
            lines.append(data["Исполнитель"] + " - " + data["Название"] + "\n")
        for line in sorted(lines):
            f.write(line)
        print(f'Успешно создан файл "{outputFileName}" из {len(lines)} mp3 файлов')
