from PIL import Image
import random
import re
import os

class half_squares(object):
    def __init__(self, pic_name, rand_pattern=None, flip=False, pixel_size=0.5, gap_factor=0.05, inverted=True):
        self.pixel_size = pixel_size #mm
        self.gap_factor = gap_factor
        self.inverted = inverted  #True looks better on cast, False looks better on extruded
        self.triangle_0 = [(self.gap_factor,self.gap_factor), (1-self.gap_factor, 1-self.gap_factor), (1-self.gap_factor, self.gap_factor)]    #upper right corner
        self.triangle_1 = [(self.gap_factor, self.gap_factor), (1-self.gap_factor, 1-self.gap_factor), (self.gap_factor, 1-self.gap_factor)]   #lower left corner
        self.triangle_2 = [(self.gap_factor,1-self.gap_factor), (1-self.gap_factor, self.gap_factor), (self.gap_factor, self.gap_factor)]      #upper left corner
        self.triangle_3 = [(self.gap_factor, 1-self.gap_factor), (1-self.gap_factor, self.gap_factor), (1-self.gap_factor, 1-self.gap_factor)] #lower right corner
        self.triangles = [self.triangle_0, self.triangle_1, self.triangle_2, self.triangle_3]
        self.screw_radius = 1.5 #mm
        self.screw_margin = 3   #mm
        self.screw_space  = 2 * (self.screw_radius + self.screw_margin) #mm

        file_full_name = pic_name
        self.flip=flip

        name_finder = re.compile("(\w+)\.(\w+)")
        file_name_only = name_finder.match(file_full_name).group(1)
        self.input_image = Image.open(r"pics/" + file_full_name)
        self.input_image_conv = self.input_image.convert("1")
        self.input_image_data =  list(self.input_image_conv.getdata())
        self.row_num , self.column_num = self.input_image.size
        self.rand_pattern = rand_pattern
        self.comp_pattern = [[True for i in range(self.column_num)] for j in range(self.row_num)]

        if not os.path.exists(os.path.dirname(r"result/" + file_name_only + r"/")):
            os.makedirs(os.path.dirname(r"result/" + file_name_only + r"/"))
        self.vectoric_rand = open(r"result/" + file_name_only + r"/" + file_name_only + r"_r.svg",'w')
        self.vectoric_preview = open(r"result/" + file_name_only + r"/" + file_name_only + r"_preview.svg", 'w')
        self.vectoric_comp = open(r"result/" + file_name_only + r"/" + file_name_only + r"_c_flipped.svg", 'w')

        self.width  = self.row_num * self.pixel_size + 2 * self.screw_space
        self.height = self.column_num * self.pixel_size + 2 * self.screw_space
        header = '<svg \n\twidth="{}mm"\n\theight="{}mm"\n\tviewBox="0 0 {} {}"\n\tversion="1.1" \
        xmlns:dc="http://purl.org/dc/elements/1.1/"\n xmlns:cc="http://creativecommons.org/ns#"\n \
        xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n xmlns:svg="http://www.w3.org/2000/svg"\n \
        xmlns="http://www.w3.org/2000/svg"\n xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd">\n'.format(
            self.width,
            self.height,
            self.width,
            self.height)
        self.vectoric_rand.write(header)
        self.vectoric_preview.write(header)
        self.vectoric_comp.write(header)

        #generate the rand and complementary patterns
        self.create_randomized_pattern()
        self.create_complementary_pattern()

    def create_randomized_pattern(self):
        if not self.rand_pattern:
            self.rand_pattern = [[True for i in range(self.column_num)] for j in range(self.row_num)]
            for row in range(self.row_num):
                for col in range(self.column_num):
                    self.rand_pattern[row][col] = random.choice([0,1,2,3])

    def create_complementary_pattern(self):
        for row in range(self.row_num):
            for col in range(self.column_num):
                if not self.inverted:
                    if self.input_image_data[col * self.row_num + row]:
                        self.comp_pattern[row][col] = self.rand_pattern[row][col]
                    else:
                        self.comp_pattern[row][col] = self.get_comp(self.rand_pattern[row][col])
                else:
                    if self.input_image_data[col * self.row_num + row]:
                        self.comp_pattern[row][col] = self.get_comp(self.rand_pattern[row][col])
                    else:
                        self.comp_pattern[row][col] = self.rand_pattern[row][col]

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
        x1 = self.pixel_size * (flipped * self.row_num + (1 - 2 * flipped) * (row + self.triangles[tri_num][0][0])) + self.screw_space
        y1 = self.pixel_size * (col + self.triangles[tri_num][0][1]) + self.screw_space
        x2 = self.pixel_size * (flipped * self.row_num + (1 - 2 * flipped) * (row + self.triangles[tri_num][1][0])) + self.screw_space
        y2 = self.pixel_size * (col + self.triangles[tri_num][1][1]) + self.screw_space
        x3 = self.pixel_size * (flipped * self.row_num + (1 - 2 * flipped) * (row + self.triangles[tri_num][2][0])) + self.screw_space
        y3 = self.pixel_size * (col + self.triangles[tri_num][2][1]) + self.screw_space
        return '\t\t<polygon points="{},{}  {},{}  {},{}" style="stroke:black;fill:none;stroke-width:0.1" />\n'.format(x1,y1,x2,y2,x3,y3)

    def add_svg_addons(self):
        circle_1 = '\t\t<circle cx="{}" cy="{}" r="{}" stroke="red" stroke-width="0.1" fill="none" />\n'.format(
            self.screw_space / 2.0,
            self.screw_space / 2.0,
            self.screw_radius)
        circle_2 = '\t\t<circle cx="{}" cy="{}" r="{}" stroke="red" stroke-width="0.1" fill="none" />\n'.format(
            self.width - self.screw_space / 2.0,
            self.screw_space / 2.0,
            self.screw_radius)
        circle_3 = '\t\t<circle cx="{}" cy="{}" r="{}" stroke="red" stroke-width="0.1" fill="none" />\n'.format(
            self.screw_space / 2.0,
            self.height - self.screw_space / 2.0,
            self.screw_radius)
        circle_4 = '\t\t<circle cx="{}" cy="{}" r="{}" stroke="red" stroke-width="0.1" fill="none" />\n'.format(
            self.width - self.screw_space / 2.0,
            self.height - self.screw_space / 2.0,
            self.screw_radius)
        circle_5 = '\t\t<circle cx="{}" cy="{}" r="{}" stroke="red" stroke-width="0.1" fill="none" />\n'.format(
            self.width / 2.0,
            self.screw_space / 2.0,
            self.screw_radius)
        circle_6 = '\t\t<circle cx="{}" cy="{}" r="{}" stroke="red" stroke-width="0.1" fill="none" />\n'.format(
            self.screw_space / 2.0,
            self.height / 2.0,
            self.screw_radius)
        circle_7 = '\t\t<circle cx="{}" cy="{}" r="{}" stroke="red" stroke-width="0.1" fill="none" />\n'.format(
            self.width / 2.0,
            self.height - self.screw_space / 2.0,
            self.screw_radius)
        circle_8 = '\t\t<circle cx="{}" cy="{}" r="{}" stroke="red" stroke-width="0.1" fill="none" />\n'.format(
            self.width - self.screw_space / 2.0,
            self.height / 2.0,
            self.screw_radius)
        rectangle = '\t\t<polygon points="{},{}  {},{}  {},{}  {},{}" style="stroke:red;fill:none;stroke-width:0.1" />\n'.format(
            0, 0,
            self.width, 0,
            self.width, self.height,
            0, self.height)

        return rectangle + circle_1 + circle_2 + circle_3 + circle_4 + circle_5 + circle_6 + circle_7 + circle_8

    def create_images(self, flip=1):
        for row in range(self.row_num):
            for col in range(self.column_num):
                if self.rand_pattern[row][col] == 0:
                    self.vectoric_rand.write(self.get_svg_triangle(0,row,col))
                    self.vectoric_preview.write(self.get_svg_triangle(0, row, col))
                elif self.rand_pattern[row][col] == 1:
                    self.vectoric_rand.write(self.get_svg_triangle(1, row, col))
                    self.vectoric_preview.write(self.get_svg_triangle(1, row, col))
                elif self.rand_pattern[row][col] == 2:
                    self.vectoric_rand.write(self.get_svg_triangle(2, row, col))
                    self.vectoric_preview.write(self.get_svg_triangle(2, row, col))
                elif self.rand_pattern[row][col] == 3:
                    self.vectoric_rand.write(self.get_svg_triangle(3, row, col))
                    self.vectoric_preview.write(self.get_svg_triangle(3, row, col))

                # flip is for thick materials (perspex etc), thin materials (paper etc) shouldn't be flipped
                if self.comp_pattern[row][col] == 0:
                    self.vectoric_preview.write(self.get_svg_triangle(0, row, col))
                    self.vectoric_comp.write(self.get_svg_triangle(0, row, col, self.flip))
                elif self.comp_pattern[row][col] == 1:
                    self.vectoric_preview.write(self.get_svg_triangle(1, row, col))
                    self.vectoric_comp.write(self.get_svg_triangle(1, row, col, self.flip))
                elif self.comp_pattern[row][col] == 2:
                    self.vectoric_preview.write(self.get_svg_triangle(2, row, col))
                    self.vectoric_comp.write(self.get_svg_triangle(2, row, col, self.flip))
                elif self.comp_pattern[row][col] == 3:
                    self.vectoric_preview.write(self.get_svg_triangle(3, row, col))
                    self.vectoric_comp.write(self.get_svg_triangle(3, row, col, self.flip))

        addons = self.add_svg_addons()

        self.vectoric_rand.write(addons + "</svg>")
        self.vectoric_preview.write(addons + "</svg>")
        self.vectoric_comp.write(addons + "</svg>")

        self.vectoric_rand.close()
        self.vectoric_preview.close()
        self.vectoric_comp.close()


if __name__ == '__main__':
    pixel_size=1#0.5
    gap_factor=0.2#0.35
    b1 = half_squares(pic_name="quote1_s.PNG", rand_pattern=None, flip=False, pixel_size=pixel_size, gap_factor=gap_factor)
    b2 = half_squares(pic_name="quote2_s.PNG", rand_pattern=b1.comp_pattern, flip=False, pixel_size=pixel_size, gap_factor=gap_factor)
    b3 = half_squares(pic_name="quote3_s.PNG", rand_pattern=b2.comp_pattern, flip=False, pixel_size=pixel_size, gap_factor=gap_factor)

    b1.create_images()
    b2.create_images()
    b3.create_images()
