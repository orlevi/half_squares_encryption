from PIL import Image
import random

class half_squares:
    def __init__(self):
        self.pixel_size = 1 #mm
        self.triangle_0 = [(0,0),(1,1),(1,0)] #upper right corner
        self.triangle_1 = [(0,0),(1,1),(0,1)] #lower left corner
        self.triangle_2 = [(0,1),(1,0),(0,0)] #upper left corner
        self.triangle_3 = [(0,1),(1,0),(1,1)] #lower right corner
        self.triangles = [self.triangle_0, self.triangle_1, self.triangle_2, self.triangle_3]
        self.aligner_radius = 1.5 #mm
        self.aligner_margin = 0.5 #mm
        self.aligner_space  = 2 * (self.aligner_radius + self.aligner_margin) #mm

        self.input_image = Image.open(r"name4.png")
        self.input_image_conv = self.input_image.convert("1")
        self.input_image_data =  list(self.input_image_conv.getdata())
        self.row_num , self.column_num = self.input_image.size
        self.rand_pattern = [[True for i in range(self.column_num)] for j in range(self.row_num)]
        self.comp_pattern = [[True for i in range(self.column_num)] for j in range(self.row_num)]

        self.vectoric_rand = open(r"vectoric_rand.svg",'w')
        self.vectoric_comp = open(r"vectoric_comp.svg",'w')
        self.vectoric_comp_flipped = open(r"vectoric_comp_flipped.svg",'w')

        self.width = self.row_num * self.pixel_size + 2 * self.aligner_space
        self.height = self.column_num * self.pixel_size
        header = '<svg \n\twidth="{}mm"\n\theight="{}mm"\n\tviewBox="0 0 {} {}"\n\tversion="1.1" >\n'.format(
            self.width,
            self.height,
            self.width,
            self.height)
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
        x1 = self.pixel_size * (flipped * self.row_num + (1 - 2 * flipped) * (row + self.triangles[tri_num][0][0]) + self.aligner_space)
        y1 = self.pixel_size * (col + self.triangles[tri_num][0][1])
        x2 = self.pixel_size * (flipped * self.row_num + (1 - 2 * flipped) * (row + self.triangles[tri_num][1][0]) + self.aligner_space)
        y2 = self.pixel_size * (col + self.triangles[tri_num][1][1])
        x3 = self.pixel_size * (flipped * self.row_num + (1 - 2 * flipped) * (row + self.triangles[tri_num][2][0]) + self.aligner_space)
        y3 = self.pixel_size * (col + self.triangles[tri_num][2][1])
        return '\t\t<polygon points="{},{}  {},{}  {},{}" />\n'.format(x1,y1,x2,y2,x3,y3)

    def add_svg_aligners(self):
        circle_1 = '\t\t<circle cx="{}" cy="{}" r="{}" stroke="red" stroke-width="0.1" fill="none" />\n'.format(
            self.aligner_space / 2.0,
            self.aligner_space / 2.0,
            self.aligner_radius)
        circle_2 = '\t\t<circle cx="{}" cy="{}" r="{}" stroke="red" stroke-width="0.1" fill="none" />\n'.format(
            self.width - self.aligner_space / 2.0,
            self.aligner_space / 2.0,
            self.aligner_radius)
        hor_1 = '\t\t<line x1="{}" y1="{}" x2="{}" y2="{}" style="stroke:red;stroke-width:0.1" />\n'.format(
            self.aligner_margin,
            self.aligner_space / 2.0,
            2 * self.aligner_radius + self.aligner_margin,
            self.aligner_space / 2.0)
        hor_2 = '\t\t<line x1="{}" y1="{}" x2="{}" y2="{}" style="stroke:red;stroke-width:0.1" />\n'.format(
            self.width - self.aligner_margin,
            self.aligner_space / 2.0,
            self.width - (2 * self.aligner_radius + self.aligner_margin),
            self.aligner_space / 2.0)
        ver_1 = '\t\t<line x1="{}" y1="{}" x2="{}" y2="{}" style="stroke:red;stroke-width:0.1" />\n'.format(
            self.aligner_space / 2.0,
            self.aligner_margin,
            self.aligner_space / 2.0,
            2 * self.aligner_radius + self.aligner_margin)
        ver_2 = '\t\t<line x1="{}" y1="{}" x2="{}" y2="{}" style="stroke:red;stroke-width:0.1" />\n'.format(
            self.width - self.aligner_space / 2.0,
            self.aligner_margin,
            self.width - self.aligner_space / 2.0,
            2 * self.aligner_radius + self.aligner_margin)
        return circle_1 + hor_1 + ver_1 + circle_2 + hor_2 + ver_2

    def create_images(self):
        for row in range(self.row_num):
            for col in range(self.column_num):
                if self.rand_pattern[row][col] == 0:
                    self.vectoric_rand.write(self.get_svg_triangle(0,row,col))
                elif self.rand_pattern[row][col] == 1:
                    self.vectoric_rand.write(self.get_svg_triangle(1, row, col))
                elif self.rand_pattern[row][col] == 2:
                    self.vectoric_rand.write(self.get_svg_triangle(2, row, col))
                elif self.rand_pattern[row][col] == 3:
                    self.vectoric_rand.write(self.get_svg_triangle(3, row, col))

                if self.comp_pattern[row][col] == 0:
                    self.vectoric_comp.write(self.get_svg_triangle(0, row, col))
                    self.vectoric_comp_flipped.write(self.get_svg_triangle(0, row, col, 1))
                elif self.comp_pattern[row][col] == 1:
                    self.vectoric_comp.write(self.get_svg_triangle(1, row, col))
                    self.vectoric_comp_flipped.write(self.get_svg_triangle(1, row, col, 1))
                elif self.comp_pattern[row][col] == 2:
                    self.vectoric_comp.write(self.get_svg_triangle(2, row, col))
                    self.vectoric_comp_flipped.write(self.get_svg_triangle(2, row, col, 1))
                elif self.comp_pattern[row][col] == 3:
                    self.vectoric_comp.write(self.get_svg_triangle(3, row, col))
                    self.vectoric_comp_flipped.write(self.get_svg_triangle(3, row, col, 1))

        aligners = self.add_svg_aligners()

        self.vectoric_rand.write(aligners + "</svg>")
        self.vectoric_comp.write(aligners + "</svg>")
        self.vectoric_comp_flipped.write(aligners + "</svg>")
        self.vectoric_rand.close()
        self.vectoric_comp.close()
        self.vectoric_comp_flipped.close()


if __name__ == '__main__':
    b = half_squares()
    b.create_randomized_pattern()
    b.create_complementary_pattern()
    b.create_images()