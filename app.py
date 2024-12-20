import pygame, random

class Cell:
    def __init__(self):
        self.id = 0
        self.occupied = False
        self.dirty = False     
    def get_color(self):
        if self.id == 1:
            return (255, 255, 0)
        if self.id == 2:
            return (0, 0, 255)
        return (0, 0, 0)

class Box:
    def __init__(self, rows, columns):
        self.hover_id = 0
        self.rows = rows
        self.columns = columns
        self.cell_size = 2
        self.cells = [[Cell() for _ in range(columns)] for _ in range(rows)]
    def draw(self, screen):
        updated_rects = []
        drawn_cells = 0
        total_cells = self.rows * self.columns
        for row in range(self.rows):
            for col in  range(self.columns):
                current_cell = self.cells[row][col]
                if current_cell.dirty:
                    drawn_cells += 1
                    x = col * self.cell_size
                    y = row * self.cell_size
                    pygame.draw.rect(screen, current_cell.get_color(), (x, y, self.cell_size, self.cell_size))
                    current_cell.dirty = False
                    updated_rects.append(pygame.Rect(x, y, self.cell_size, self.cell_size))
        pygame.display.update(updated_rects)    
        
        if total_cells > 0:
            draw_ratio = drawn_cells / total_cells * 100  # Tính tỷ lệ phần trăm
            print(f"Tỷ lệ cells đang draw: {draw_ratio:.2f}%", end='\r')       
    def position_in_box(self, row, col):
        return 0 <= col < self.columns and 0 <= row < self.rows
    def handle_click(self, pos):
        x, y = pos
        col = x // self.cell_size
        row = y // self.cell_size
        for i in range(row - 5, row + 5):
            for j in range(col - 5, col + 5):
                if self.position_in_box(i, j):
                    current_cell = self.cells[i][j]
                    if not current_cell.occupied:
                        current_cell.occupied = True
                        current_cell.id = self.hover_id
                        current_cell.dirty = True       
    def reset_screen(self, screen):
        updated_rects = []
        for row in range(self.rows):
            for col in range(self.columns):
                current_cell = self.cells[row][col]
                if not self.empty_cell(current_cell):
                    x = col * self.cell_size
                    y = row * self.cell_size
                    pygame.draw.rect(screen, (0, 0, 0), (x, y, self.cell_size, self.cell_size))
                    current_cell.id = 0
                    current_cell.occupied = False
                    current_cell.dirty = False
                    updated_rects.append(pygame.Rect(x, y, self.cell_size, self.cell_size))
        pygame.display.update(updated_rects)
    def handle_hover(self, pos):
        x, y = pos
        col = x // self.cell_size
        row = y // self.cell_size
        
        if self.position_in_box(row, col):
            current_cell = self.cells[row][col]
            if not current_cell.occupied:
                current_cell.occupied = True
                current_cell.id = self.hover_id
                current_cell.dirty = True
    def falling_vertical(self, current, below):
        below.id = current.id
        below.occupied = True
        current.id = 0
        current.occupied = False    
    def lower_cell_identify(self, row, col):
        self.lower_left_cell = None
        self.lower_right_cell = None
        if col > 0:
            self.lower_left_cell = self.cells[row + 1][col - 1]
        if col < self.columns - 1:
            self.lower_right_cell = self.cells[row + 1][col + 1]           
    def equal_cell_identify(self, row, col):
        self.equal_left_cell = None
        self.equal_right_cell = None
        if col > 0:
            self.equal_left_cell = self.cells[row][col - 1]
        if col < self.columns - 1:
            self.equal_right_cell = self.cells[row][col + 1]         
    def swap_cell(self, first_cell, second_cell):
        temp_id = first_cell.id
        temp_occupied = first_cell.occupied
        first_cell.id = second_cell.id
        first_cell.occupied = second_cell.occupied
        second_cell.id = temp_id
        second_cell.occupied = temp_occupied
        
        first_cell.dirty = True
        second_cell.dirty = True       
    def exist_cell(self, forecast_cell):
        if forecast_cell:
            return True
        return False
    def sand_is(self, current_cell):
        return current_cell.id == 1      
    def water_is(self, cell):
        return cell.id == 2   
    def empty_cell(self, cell):
        return cell.id == 0
    def branching_down(self, current_cell):
        
        if not self.empty_cell(current_cell):
            free_cells = []
            
            if self.exist_cell(self.lower_left_cell) and not self.lower_left_cell.occupied:
                free_cells.append(self.lower_left_cell)
            elif self.exist_cell(self.lower_left_cell) and self.sand_is(current_cell) and self.water_is(self.lower_left_cell):
                free_cells.append(self.lower_left_cell)
                
            if self.exist_cell(self.lower_right_cell) and not self.lower_right_cell.occupied:
                free_cells.append(self.lower_right_cell)
            elif self.exist_cell(self.lower_right_cell) and self.sand_is(current_cell) and self.water_is(self.lower_right_cell):
                free_cells.append(self.lower_right_cell)

            if free_cells:
                random_cell = random.choice(free_cells)
                self.swap_cell(current_cell, random_cell)   
    def distance_position(cls, y, x):
        return abs(x - y)        
    def branching_water(self, row, col, current_cell):
        free_cells = []
        left_cell = False
        right_cell = False
        left_pos = None
        right_pos = None
        for i in range(col, -1, -1):
            cell_below_range_left = self.cells[row + 1][i]
            if self.empty_cell(cell_below_range_left):
                left_cell = True
                left_pos = i
                break         
        for i in range(col, self.columns):
            cell_below_range_right = self.cells[row + 1][i]
            if self.empty_cell(cell_below_range_right):
                right_cell = True
                right_pos = i
                break
            
        if left_cell and right_cell:
            dist_left = self.distance_position(left_pos, col)
            dist_right = self.distance_position(col, right_pos)
            if not self.cells[row][left_pos + 1].occupied:
                self.equal_left_cell = self.cells[row][left_pos + 1]
            if not self.cells[row][left_pos - 1].occupied:
                self.equal_right_cell = self.cells[row][right_pos - 1]
            
            if dist_left < dist_right and self.empty_cell(self.equal_left_cell):
                free_cells.append(self.equal_left_cell)
            elif dist_left > dist_right and self.empty_cell(self.equal_right_cell):
                free_cells.append(self.equal_right_cell)  
            else:
                if self.empty_cell(self.equal_left_cell):
                    free_cells.append(self.equal_left_cell)  
                if self.empty_cell(self.equal_right_cell):
                    free_cells.append(self.equal_right_cell)   
        elif left_cell and self.empty_cell(self.equal_left_cell):
            free_cells.append(self.equal_left_cell)
        elif right_cell and self.empty_cell(self.equal_right_cell):
            free_cells.append(self.equal_right_cell)
                
        if free_cells:
            random_cell = random.choice(free_cells)
            random_cell.id = current_cell.id
            random_cell.occupied = True
            current_cell.id = 0
            current_cell.occupied = False
            current_cell.dirty = True
            random_cell.dirty = True              
    def falling(self):
        for row in range(self.rows - 1, -1, -1):
            for col in range(self.columns - 1, -1, -1):
                if self.cells[row][col].occupied:
                    if row < self.rows - 1:
                        current_cell = self.cells[row][col]
                        cell_below = self.cells[row + 1][col]
                        
                        if not cell_below.occupied:
                            if current_cell.id != 3 and current_cell.id != 0:
                                self.falling_vertical(current_cell, cell_below)
                                current_cell.dirty = True
                                cell_below.dirty = True
                        else:      
                            if cell_below.id == 1 or cell_below.id == 2:
                                self.equal_cell_identify(row, col)
                                self.lower_cell_identify(row, col)
                                self.branching_down(current_cell)
                            if current_cell.id == 2:
                                self.branching_water(row, col, current_cell)
                            if self.water_is(cell_below) and self.sand_is(current_cell) and not self.empty_cell(self.cells[row - 1][col]):
                                self.swap_cell(cell_below, current_cell)
                                
class Game:
    def __init__(self):
        pygame.init()
        self.width = 300
        self.height = self.width
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Falling Sand")
        self.clock = pygame.time.Clock()
        self.fps = 120
                                
def main():
    game = Game()
    box = Box(game.width // 2, game.width // 2)

    running = True
    print("Chọn '0' nothing")
    print("Chọn '1' để gọi cát")
    print("Chọn '2' để gọi nước")
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0 or event.key == pygame.K_KP0:
                    box.hover_id = 0
                elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    box.hover_id = 1
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    box.hover_id = 2
                elif event.key == pygame.K_ESCAPE:
                    box.reset_screen(game.screen)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    box.handle_click(pos)

        if box.hover_id != 0:
            pos = pygame.mouse.get_pos()
            box.handle_hover(pos)
        box.falling()
        box.draw(game.screen)
            
        game.clock.tick(game.fps)

    pygame.quit()

if __name__ == "__main__":
    main()