import unittest
from shell import Shell
from vfs import VFS

class TestShell(unittest.TestCase):
    def setUp(self):
        config = {
            'user': 'user1',
            'host': 'localhost',
            'vfs_path': 'test.zip'
        }
        self.shell = Shell(config)
        self.shell.cd('/')

    def test_ls(self):
        # Test ls in root directory
        result = self.shell.ls()
        self.assertIsInstance(result, str)
        self.assertIn('test1', result)
        self.assertIn('test2', result)
        self.assertIn('test3', result)
        self.assertIn('file0', result)

        # Test ls in a specific directory
        self.shell.cd('test1')
        result = self.shell.ls()
        self.assertIsInstance(result, str)
        self.assertIn('file1.txt', result)

        self.shell.cd('..')
        self.shell.cd('test2')
        result = self.shell.ls()
        self.assertIsInstance(result, str)
        self.assertIn('file2.txt', result)
        self.assertIn('file2_2.txt', result)

        self.shell.cd('..')
        self.shell.cd('test3')
        result = self.shell.ls()
        self.assertIsInstance(result, str)
        self.assertIn('file3.txt', result)
        self.assertIn('file3_3.txt', result)

    def test_cd(self):
        # Test cd to existing directory
        result = self.shell.cd('test')
        self.assertIn('Current directory ', result)

        # Test cd to non-existing directory
        result = self.shell.cd('non_existing_directory')
        self.assertIn('cd: no such directory', result)

        # Test cd to parent directory
        self.shell.cd('test')
        result = self.shell.cd('..')
        self.assertIn('Current directory ', result)

    def test_touch(self):
        # Test touch to create a new file
        result = self.shell.touch('newfile.txt')  # Команда touch для создания нового файла
        self.assertIn('File created', result)  # Проверка, что файл был создан

        # Test touch on existing file (should not create it again)
        result = self.shell.touch('newfile.txt')
        self.assertIn('File already exists', result)  # Проверка, что файл уже существует

    def test_rm(self):
        # Test rm to delete an existing file
        self.shell.touch('file_to_delete.txt')  # Сначала создаем файл
        result = self.shell.rm('file_to_delete.txt')  # Команда rm для удаления файла
        self.assertIn('File deleted', result)  # Проверка, что файл был удален

        # Test rm to delete a non-existing file
        result = self.shell.rm('non_existing_file.txt')  # Пытаемся удалить несуществующий файл
        self.assertIn('File not found', result)  # Проверка, что выводится ошибка

    def test_exit(self):
        # Test exit command
        result = self.shell.exit()  # Команда exit для выхода
        self.assertIn('Exiting shell', result)  # Проверка, что выводится сообщение о выходе

    def tearDown(self):
        # Это выполняется после каждого теста (если нужно очистить тестовое окружение)
        pass

if __name__ == '__main__':
    unittest.main()