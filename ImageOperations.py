from math import sqrt


class ImageOperations:

    def __init__(self) -> None:
        pass

    def load_image(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
        except FileNotFoundError:
            print(f"O arquivo {file_path} não foi encontrado.")
        except Exception as e:
            print(f"Ocorreu um erro ao abrir o arquivo: {e}")

        file.close()

        content = content.split("\n")

        return content

    def save_image(self, content, path):
        try:
            with open(path, 'w') as file:
                if isinstance(content, str):
                    file.write(content)
                else:
                    file.write('\n'.join(content))
            print(f'O arquivo {path} foi salvo com sucesso.')
        except Exception as e:
            print(f'Ocorreu um erro ao salvar o arquivo: {e}')

    def filter_negative(self, content):
        new_content = content[:4]
        for value in content[4:]:
            if value != '':
                new_value = 255 - int(value)
            new_content.append(str(new_value))

        return new_content

    def filter_threshold(self, content, threshold):
        new_content = content[:4]
        for value in content[4:]:
            if value != '':
                if int(value) <= threshold:
                    new_value = 0
                else:
                    new_value = 255
            new_content.append(str(new_value))

        return new_content
    
    def calculate_histogram(self, content):
        histogram = [0]*256

        for intensity in content[4:]:
            if intensity != "":
                histogram[int(intensity)] += 1
        return histogram
    
    def create_histogram_image(self, histogram, path):
        maxCount = max(histogram)
        width, height = 256, maxCount
        matrix = [[0 for _ in range(width)] for _ in range(height)]

        for j in range(width):
            count = histogram[j]
            for i in range(maxCount-1, maxCount-count-1, -1):
                # print(image)
                matrix[i][j] = 1

        image = "P1\n" + f'{width} {height}\n'

        for line in matrix:
            line = [str(x) for x in line]
            image += ' '.join(line) + "\n"

        self.save_image(image, path) 

    
    def print_histogram(self, histogram):
        
        for i in range(len(histogram)):
            print(f'{i}: {histogram[i]}')

    def equalize_image(self, file_path, new_path):
        original_image = self.load_image(file_path)
        histogram = self.calculate_histogram(original_image)
        pixels_count = len(original_image)

        normalized_histogram = [x/pixels_count for x in histogram]
        
        cumulative_distribuition = [0]*256

        sum = 0
        for i in range(256):
            cumulative_distribuition[i] = sum + normalized_histogram[i]
            sum += normalized_histogram[i]

        new_colors = [round(x*255) for x in cumulative_distribuition]

        new_image = original_image[:4]
        
        for color in original_image[4:]:
            new_color = str(new_colors[int(color)])
            new_image.append(new_color)
        
        self.save_image(new_image, new_path)

    def calculate_average(self, i, j, matrix, distance):
        n = (distance*2 + 1)**2
        max_n, max_m = len(matrix)-1, len(matrix[0])-1
        # where_to_look = [(i,j), (i-1,j), (i-1,j-1), (i, j-1), (i+1, j), (i+1, j+1), (i, j+1), (i-1, j+1), (i+1, j-1)]

        average = 0
        default = 128

        where_to_look = []

        for i in range(i - distance, i + distance + 1):
            for j in range(j - distance, j + distance + 1):
                where_to_look.append((i, j))
                if i < 0 or j < 0 or i > max_n or j > max_m:
                    average += default
                else:
                    average += int(matrix[i][j])

        return average / n
    
    def get_matrix_from_array(self, arr):
        matrix = []
        n = int(sqrt(len(arr)))
    
        for i in range(n):
            a = i*n
            b = i*n + n
            matrix.append(arr[a:b])

        return matrix
    
    def smoothing_filter(self, file_path, new_path, n):
        original_image = self.load_image(file_path)
        info = original_image[:4]
        content = original_image[4:]
        content_matrix = self.get_matrix_from_array(content)

        width, height = [int(x) for x in info[2].split(' ')]
        
        new_image = [['' for _ in range(width)] for _ in range(height)]

        for i in range(height):
            for j in range(width):
                new_image[i][j] = str(self.calculate_average(i, j, content_matrix, n))

        new_image = '\n'.join(info) + '\n' + '\n'.join([' '.join(line) for line in new_image])
        self.save_image(new_image, new_path)