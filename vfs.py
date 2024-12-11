import zipfile
import io

class VFS:
    def __init__(self, zip_path):
        # Открытие архива в режиме чтения ('r') и записи ('a') для добавления файлов
        self.zip_path = zip_path
        self.zip_file = zipfile.ZipFile(zip_path, 'a')  # Открытие архива в режиме 'a' (append)
        self.current_path = '/'

    def list_dir(self, path):
        try:
            all_files = self.zip_file.namelist()  # Получаем список всех файлов в архиве
            normalized_path = path.lstrip('/')  # Убираем начальный "/"

            if normalized_path and not normalized_path.endswith('/'):
                normalized_path += '/'  # Убедимся, что путь заканчивается "/"

            contents = set()
            for file in all_files:
                if file.startswith(normalized_path):  # Проверяем, лежит ли файл в каталоге
                    relative_path = file[len(normalized_path):].lstrip('/')
                    first_part = relative_path.split('/')[0]
                    if first_part:
                        contents.add(first_part)  # Добавляем уникальные файлы/папки в результат

            return sorted(contents)
        except Exception as e:
            raise Exception(f"Error reading directory '{path}': {str(e)}")

    def list_files(self, path):
        # Получение списка файлов в заданной директории
        return [file for file in self.zip_file.namelist() if file.startswith(path)]

    def read_file(self, path):
        try:
            with self.zip_file.open(path) as f:
                return f.read().decode('utf-8')
        except KeyError:
            raise KeyError(f"There is no file named '{path}' in the archive")
        except Exception as e:
            raise Exception(f"Error reading file '{path}': {str(e)}")

    def directory_exists(self, path):
        normalized_path = path.lstrip('/')
        if not normalized_path.endswith('/'):
            normalized_path += '/'
        return any(file.startswith(normalized_path) for file in self.zip_file.namelist())

    def file_exists(self, path):
        # Проверяет, существует ли файл в архиве
        normalized_path = path.lstrip('/')
        return normalized_path in self.zip_file.namelist()

    def create_file(self, path):
        # Создаёт пустой файл в архиве
        normalized_path = path.lstrip('/')
        if self.file_exists(normalized_path):
            raise FileExistsError(f"File '{normalized_path}' already exists in the archive")

        # Создаем пустой файл в архиве
        with zipfile.ZipFile(self.zip_path, mode='a') as zipf:
            zipf.writestr(normalized_path, '')  # Создаем пустой файл

    def delete_file(self, path):
        # Удаляет файл из архива
        normalized_path = path.lstrip('/')
        if not self.file_exists(normalized_path):
            raise FileNotFoundError(f"File '{normalized_path}' does not exist in the archive")

        # Создаем временный архив в памяти, в который будут записаны все файлы, кроме удаляемого
        temp_buffer = io.BytesIO()
        with zipfile.ZipFile(temp_buffer, mode='w') as temp_zip:
            for item in self.zip_file.infolist():
                if item.filename != normalized_path:
                    # Копируем все файлы, кроме удаляемого
                    temp_zip.writestr(item, self.zip_file.read(item.filename))

        # Перезаписываем оригинальный архив новым содержимым
        with open(self.zip_path, 'wb') as f:
            f.write(temp_buffer.getvalue())

        # Открываем обновленный архив
        self.zip_file = zipfile.ZipFile(self.zip_path, mode='a')

    def close(self):
        self.zip_file.close()