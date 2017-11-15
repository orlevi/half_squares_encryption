from PIL import Image
import random

class half_squares:
    def __init__(self):
        self.pixel_size = 0.5 #mm
        self.triangle_0 = [(0,0),(1,1),(1,0)]
        self.triangle_1 = [(0,0),(1,1),(0,1)]
        self.triangle_2 = [(0,1),(1,0),(0,0)]
        self.triangle_3 = [(0,1),(1,0),(1,1)]
        self.triangles = [self.triangle_0, self.triangle_1, self.triangle_2, self.triangle_3]

        self.image_0 = Image.open(r"C:\Users\Or Levi\PycharmProjects\half_squares_encryption\half_square_0_i.png")
        self.image_1 = Image.open(r"C:\Users\Or Levi\PycharmProjects\half_squares_encryption\half_square_1_i.png")
        self.image_2 = Image.open(r"C:\Users\Or Levi\PycharmProjects\half_squares_encryption\half_square_2_i.png")
        self.image_3 = Image.open(r"C:\Users\Or Levi\PycharmProjects\half_squares_encryption\half_square_3_i.png")
        self.input_image = Image.open(r"C:\Users\Or Levi\PycharmProjects\half_squares_encryption\name7.png")
        self.input_image_conv = self.input_image.convert("1")
        self.input_image_data =  list(self.input_image_conv.getdata())
        self.row_num , self.column_num = self.input_image.size
        self.rand_pattern = [[True for i in range(self.column_num)] for j in range(self.row_num)]
        self.comp_pattern = [[True for i in range(self.column_num)] for j in range(self.row_num)]
        self.rand_pattern_image = Image.new("1",(self.row_num * 5, self.column_num * 5))
        self.comp_pattern_image = Image.new("1",(self.row_num * 5, self.column_num * 5))
        self.comp_flipped_image = Image.new("1",(self.row_num * 5, self.column_num * 5))

        self.vectoric_rand = open(r"C:\Users\Or Levi\PycharmProjects\half_squares_encryption\vectoric_rand.svg",'w')
        self.vectoric_comp = open(r"C:\Users\Or Levi\PycharmProjects\half_squares_encryption\vectoric_comp.svg",'w')
        self.vectoric_comp_flipped = open(r"C:\Users\Or Levi\PycharmProjects\half_squares_encryption\vectoric_comp_flipped.svg",'w')
        header = '<svg \n\twidth="{}mm"\n\theight="{}mm"\n\tviewBox="0 0 {} {}"\n\tversion="1.1" >\n'.format(self.row_num * self.pixel_size,
                                                                                                           self.column_num * self.pixel_size,
                                                                                                           self.row_num * self.pixel_size,
                                                                                                           self.column_num * self.pixel_size)
        self.vectoric_rand.write(header)
        self.vectoric_comp.write(header)
        self.vectoric_comp_flipped.write(header)

    def create_randomized_pattern(self):
        for row in range(self.row_num):
            for col in range(self.column_num):
                self.rand_pattern[row][col] = random.choice([0,1,2,3])

    def create_complementary_pattern(self):
        for row in range(self.row_num):
            for col in range(self.column_num):
                if self.input_image_data[col * self.row_num + row]:
                    self.comp_pattern[row][col] = self.rand_pattern[row][col]
                else:
                    self.comp_pattern[row][col] = self.get_comp(self.rand_pattern[row][col])

    def get_comp(self, pat):
        if pat == 0:
            return 1
        elif pat == 1:
            return 0
        elif pat == 2:
            return 3
        elif pat == 3:
            return 2

    def get_svg_triangle(self,tri_num,row,col,flipped = 0):
        x1 = self.pixel_size * (flipped * self.row_num + (1 - 2 * flipped) * (row + self.triangles[tri_num][0][0]))
        y1 = self.pixel_size * (col + self.triangles[tri_num][0][1])
        x2 = self.pixel_size * (flipped * self.row_num + (1 - 2 * flipped) * (row + self.triangles[tri_num][1][0]))
        y2 = self.pixel_size * (col + self.triangles[tri_num][1][1])
        x3 = self.pixel_size * (flipped * self.row_num + (1 - 2 * flipped) * (row + self.triangles[tri_num][2][0]))
        y3 = self.pixel_size * (col + self.triangles[tri_num][2][1])
        return '\t\t<polygon points="{},{}  {},{}  {},{}" />\n'.format(x1,y1,x2,y2,x3,y3)

    def create_images(self):
        for row in range(self.row_num):
            for col in range(self.column_num):
                if self.rand_pattern[row][col] == 0:
                    self.rand_pattern_image.paste(self.image_0, (row * 5, col * 5))
                    self.vectoric_rand.write(self.get_svg_triangle(0,row,col))
                elif self.rand_pattern[row][col] == 1:
                    self.rand_pattern_image.paste(self.image_1, (row * 5, col * 5))
                    self.vectoric_rand.write(self.get_svg_triangle(1, row, col))
                elif self.rand_pattern[row][col] == 2:
                    self.rand_pattern_image.paste(self.image_2, (row * 5, col * 5))
                    self.vectoric_rand.write(self.get_svg_triangle(2, row, col))
                elif self.rand_pattern[row][col] == 3:
                    self.rand_pattern_image.paste(self.image_3, (row * 5, col * 5))
                    self.vectoric_rand.write(self.get_svg_triangle(3, row, col))

                if self.comp_pattern[row][col] == 0:
                    self.comp_pattern_image.paste(self.image_0, (row * 5, col * 5))
                    self.vectoric_comp.write(self.get_svg_triangle(0, row, col))
                    self.vectoric_comp_flipped.write(self.get_svg_triangle(0, row, col, 1))
                elif self.comp_pattern[row][col] == 1:
                    self.comp_pattern_image.paste(self.image_1, (row * 5, col * 5))
                    self.vectoric_comp.write(self.get_svg_triangle(1, row, col))
                    self.vectoric_comp_flipped.write(self.get_svg_triangle(1, row, col, 1))
                elif self.comp_pattern[row][col] == 2:
                    self.comp_pattern_image.paste(self.image_2, (row * 5, col * 5))
                    self.vectoric_comp.write(self.get_svg_triangle(2, row, col))
                    self.vectoric_comp_flipped.write(self.get_svg_triangle(2, row, col, 1))
                elif self.comp_pattern[row][col] == 3:
                    self.comp_pattern_image.paste(self.image_3, (row * 5, col * 5))
                    self.vectoric_comp.write(self.get_svg_triangle(3, row, col))
                    self.vectoric_comp_flipped.write(self.get_svg_triangle(3, row, col, 1))
        self.comp_flipped_image = self.comp_pattern_image.transpose(Image.FLIP_LEFT_RIGHT)

        self.comp_pattern_image.save(r"C:\Users\Or Levi\PycharmProjects\half_squares_encryption\comp.png")
        self.comp_flipped_image.save(r"C:\Users\Or Levi\PycharmProjects\half_squares_encryption\comp_flipped.png")
        self.rand_pattern_image.save(r"C:\Users\Or Levi\PycharmProjects\half_squares_encryption\rand.png")
        self.vectoric_rand.write("</svg>")
        self.vectoric_comp.write("</svg>")
        self.vectoric_comp_flipped.write("</svg>")
        self.vectoric_rand.close()
        self.vectoric_comp.close()
        self.vectoric_comp_flipped.close()


if __name__ == '__main__':
    b = half_squares()
    b.create_randomized_pattern()
    b.create_complementary_pattern()
    b.create_images()