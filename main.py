import tkinter as tk, random, numpy, datetime
from PIL import Image
from tkinter import colorchooser

WIDTH_WINDOW = 700
HEIGHT_WINDOW = 700
width_maze_surface = 600
height_maze_surface = 600

class MazeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze generator")
        root.geometry(f"{WIDTH_WINDOW}x{HEIGHT_WINDOW}")
        root.resizable(False, False)
        
        # colors -> (255, 255, 255)
        self.color_wall = (0, 0, 0)
        self.color_path = (255, 255, 255)

        self.canvas = tk.Canvas(root, width=width_maze_surface, height=height_maze_surface, bg=("white"))
        self.canvas.pack()

        self.label_color_wall = tk.Label(root, text=f'Color walls: #{self.color_wall[0]:02X}{self.color_wall[1]:02X}{self.color_wall[2]:02X}', font=('Arial', 10))
        self.label_color_wall.pack(side="top", padx=10)

        self.label_color_path = tk.Label(root, text=f'Color path: #{self.color_path[0]:02X}{self.color_path[1]:02X}{self.color_path[2]:02X}', font=('Arial', 10))
        self.label_color_path.pack(side="top", padx=10)

        self.label_width = tk.Label(root, text='Size:')
        self.label_width.pack(side="left", padx=10)

        self.input_width = tk.Entry(root, width=10, textvariable=tk.StringVar(value="10"), justify='center')
        self.input_width.pack(side="left")

        self.but_maze_generate = tk.Button(root, text="Generate", command=self.new_maze)
        self.but_maze_generate.pack(side="left", padx=5)

        self.but_maze_generate = tk.Button(root, text="Save to png", command=self.save_image)
        self.but_maze_generate.pack(side="left", padx=5)

        self.var_checkbot_random_colors = tk.IntVar()
        self.but_checkbot_random_colors = tk.Checkbutton(root, text="Random colors", variable=self.var_checkbot_random_colors)
        self.but_checkbot_random_colors.pack(side="left")

        self.label_scale = tk.Label(root, text='Scale for save:')
        self.label_scale.pack(side="left", padx=5)

        self.input_scale = tk.Scale(root, from_=1, to=20, orient=tk.HORIZONTAL, length=100, resolution=1)
        self.input_scale.pack(side="left", padx=5)
        self.input_scale.set(5)

        self.but_pick_color_path = tk.Button(root, text="Color path", command=self.change_color_path)
        self.but_pick_color_path.pack(side="bottom", padx=5)

        self.but_pick_color_wall = tk.Button(root, text="Color wall", command=self.change_color_wall)
        self.but_pick_color_wall.pack(side="bottom", padx=5)

        self.maze = self.maze_generation()

        self.init_size()
        self.draw()

    def change_color_path(self):
        color = colorchooser.askcolor(title="Change color for path", initialcolor=self.color_path)
        if color[0] is not None:
            self.color_path = color[0]
            self.label_color_path.config(text=f'Color path: #{self.color_path[0]:02X}{self.color_path[1]:02X}{self.color_path[2]:02X}', fg=f'#{self.color_path[0]:02X}{self.color_path[1]:02X}{self.color_path[2]:02X}')

    def change_color_wall(self):
        color = colorchooser.askcolor(title="Change color for wall", initialcolor=self.color_wall)
        if color[0] is not None:
            self.color_wall = color[0]
            self.label_color_wall.config(text=f'Color walls: #{self.color_wall[0]:02X}{self.color_wall[1]:02X}{self.color_wall[2]:02X}', fg=f'#{self.color_wall[0]:02X}{self.color_wall[1]:02X}{self.color_wall[2]:02X}')
    
    def new_maze(self):
        self.init_size()
        self.maze = self.maze_generation(self.count_x, self.count_y)
        self.draw()

    # init size maze
    def init_size(self):
        self.count_x, self.count_y = int(self.input_width.get()), int(self.input_width.get())
        self.width_pixel = width_maze_surface / (self.count_x*2 + 1)
        self.height_pixel = height_maze_surface / (self.count_y*2 + 1)
    
    # generate maze
    def maze_generation(self, width = 10, height = 10):
        if self.var_checkbot_random_colors.get() == 1:
            self.color_path = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
            self.color_wall = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
            
            self.label_color_wall.config(text=f'Color walls: #{self.color_wall[0]:02X}{self.color_wall[1]:02X}{self.color_wall[2]:02X}', fg=f'#{self.color_wall[0]:02X}{self.color_wall[1]:02X}{self.color_wall[2]:02X}')
            self.label_color_path.config(text=f'Color path: #{self.color_path[0]:02X}{self.color_path[1]:02X}{self.color_path[2]:02X}', fg=f'#{self.color_path[0]:02X}{self.color_path[1]:02X}{self.color_path[2]:02X}')
        
        maze = numpy.full((width*2+1, height*2+1, 3), self.color_wall)
        maze[1::2, 1::2] = self.color_path
        visited = set()

        def is_valid(x, y):
            return 0 < x < width*2 and 0 < y < height*2 and (x, y) not in visited
        
        def get_neighbors(x, y):
            neingbors = []
            directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
            for dx, dy in directions:
                nx, ny = dx + x, dy + y
                if is_valid(nx, ny):
                    neingbors.append((nx, ny))
            return neingbors
        
        stack = [(1, 1)]
        visited.add((1,1))

        while stack:
            current_x, current_y = stack[-1]
            neighbors = get_neighbors(current_x, current_y)
            if neighbors:
                next_x, next_y = random.choice(neighbors)
                maze[(current_x + next_x) // 2, (current_y + next_y) // 2] = self.color_path
                visited.add((next_x, next_y))
                stack.append((next_x, next_y))
            else:
                stack.pop()
        return maze

    # draw new maze
    def draw(self):
        try:
            if self.pixels:
                for i in self.pixels:
                    self.canvas.delete(i)
        except:
            pass
        self.pixels = []
        self.init_size()
        x, y = 2, 2
        for i in self.maze:
            for r,g,b in i:
                self.color = f"#{r:02X}{g:02X}{b:02X}"
                pixel = self.canvas.create_rectangle(x, y, x+self.width_pixel, y+self.height_pixel, fill=self.color, outline=self.color)
                self.pixels.append(pixel)
                x += self.width_pixel
            x = 2
            y += self.height_pixel

    # save img maze
    def save_image(self):
        maze = (self.maze).astype(numpy.uint8)
        img = Image.fromarray(maze).resize(((self.count_x*2+1)*int(self.input_scale.get()), (self.count_y*2+1)*int(self.input_scale.get())), Image.Resampling.NEAREST)
        img.save(f"Maze_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.png", mode='R')

if __name__ == '__main__':
    root = tk.Tk()
    app = MazeGenerator(root)
    root.mainloop()