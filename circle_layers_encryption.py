from PIL import Image
import random
import re
import os


class circle_layers(object):
    def __init__(self, pic_name, inverted=False, layers_num=1, pixel_size=0.5, gap_factor=0.05):
        self.pixel_size = pixel_size #mm
        self.gap_factor = gap_factor
        self.inverted = inverted
        self.layers_num = layers_num
        self.screw_radius = 1.5 #mm
        self.screw_margin = 3   #mm
        self.screw_space  = 2 * (self.screw_radius + self.screw_margin) #mm

        file_full_name = pic_name

        name_finder = re.compile("(\w+)\.(\w+)")
        file_name_only = name_finder.match(file_full_name).group(1)
        self.input_image = Image.open(r"pics/" + file_full_name)
        self.input_image_conv = self.input_image.convert("1")
        self.input_image_data =  list(self.input_image_conv.getdata())
        self.row_num , self.column_num = self.input_image.size

        self.width = self.row_num * self.pixel_size + 2 * self.screw_space
        self.height = self.column_num * self.pixel_size + 2 * self.screw_space
        header = '<svg \n\twidth="{}mm"\n\theight="{}mm"\n\tviewBox="0 0 {} {}"\n\tversion="1.1" \
                xmlns:dc="http://purl.org/dc/elements/1.1/"\n xmlns:cc="http://creativecommons.org/ns#"\n \
                xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n xmlns:svg="http://www.w3.org/2000/svg"\n \
                xmlns="http://www.w3.org/2000/svg"\n xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd">\n'.format(
            self.width,
            self.height,
            self.width,
            self.height)

        self.layer_patterns = []
        self.vectoric_layers = []

        for layer in range(self.layers_num):
            self.layer_patterns.append([[True for i in range(self.column_num)] for j in range(self.row_num)])

        if not os.path.exists(os.path.dirname(r"result/" + file_name_only + r"/")):
            os.makedirs(os.path.dirname(r"result/" + file_name_only + r"/"))

        self.vectoric_preview = open(r"result/" + file_name_only + r"/" + file_name_only + r"_preview" + ".svg",'w')
        self.vectoric_preview.write(header)
        for layer in range(self.layers_num):
            layer_f = open(r"result/" + file_name_only + r"/" + file_name_only + r"_layer" + str(layer) + ".svg",'w')
            layer_f.write(header)
            self.vectoric_layers.append(layer_f)

        #generate the rand and complementary patterns
        self.create_patterns()

    def create_patterns(self):
        for row in range(self.row_num):
            for col in range(self.column_num):
                if not self.input_image_data[col * self.row_num + row]:
                    self.layer_patterns[random.choice(range(self.layers_num))][row][col] = False


    def get_svg_circle(self, row, col, mark_circle=False):
        if mark_circle:
            color = "red"
            width = 0.2
        else:
            color = "black"
            width = 0.1
        cx = self.pixel_size * (row + 0.5) + self.screw_space
        cy = self.pixel_size * (col + 0.5) + self.screw_space
        return '\t\t<circle cx="{}" cy="{}" r="{}" stroke="{}" stroke-width="{}" fill="none" />\n'.format(
            cx, cy, (self.pixel_size / 2.0) * (1 - self.gap_factor), color, width)

    def add_svg_addons(self):
        rectangle = '\t\t<polygon points="{},{}  {},{}  {},{}  {},{}" style="stroke:red;fill:none;stroke-width:0.1" />\n'.format(
            0, 0,
            self.width, 0,
            self.width, self.height,
            0, self.height)

        return rectangle #+ circle_1 + circle_2 + circle_3 + circle_4 + circle_5 + circle_6 + circle_7 + circle_8

    def create_images(self):
        for layer in range(self.layers_num):
            for row in range(self.row_num):
                for col in range(self.column_num):
                    if self.layer_patterns[layer][row][col]:
                        self.vectoric_layers[layer].write(self.get_svg_circle(row,col))
                        self.vectoric_preview.write(self.get_svg_circle(row, col))
                    else:
                        self.vectoric_preview.write(self.get_svg_circle(row, col, mark_circle=True))

        addons = self.add_svg_addons()

        self.vectoric_preview.write(addons + "</svg>")
        self.vectoric_preview.close()
        for vectoric_layer in self.vectoric_layers:
            vectoric_layer.write(addons + "</svg>")
            vectoric_layer.close()


if __name__ == '__main__':
    pixel_size=1#0.5
    gap_factor=0.2#0.35
    b1 = circle_layers(pic_name="achinoam_s_t.PNG", layers_num=8, pixel_size=pixel_size, gap_factor=gap_factor)

    b1.create_images()

