import itertools
import json

from src.utils import seek_get

class Object:
    SUPERBALL_BIT_POSITION = [3, 26, 27]
    SUPERBALL_CONTAINER_IDS = [5, 29, 23, 4, 30, 13]
    
    def __init__(self):
        self.id = None
        self.flag = None
        self.child_id = None
        self.child_flags = None
        self.link_id = None
        self.extended_data = None
        self.x = None
        self.y = None
        
    def __repr__(self):
        return json.dumps({
            "id": self.id,
            "x_cell": self.x,
            "y_cell": self.y,
            "flag": self.flag,
            "child_id": self.child_id,
            "child_flags": self.child_flags,
            "link_id": self.link_id,
            "extended_data": self.extended_data,
        }, indent=2)
        
    def __str__(self):
        return str(self.id)
    
    def set_id(self, o_id):
        self.id = o_id
        return self
        
    def set_flag(self, o_flag):
        self.flag = o_flag
        return self
    
    def set_child_id(self, child_id):
        self.child_id = child_id
        return self
    
    def set_child_flags(self, child_flags):
        self.child_flags = child_flags
        return self
    
    def set_link_id(self, link_id):
        self.link_id = link_id
        return self
    
    def set_extended_data(self, extended_data):
        self.extended_data = extended_data
        return self
    
    def set_coords(self, x_pos, y_pos):
        def convert_to_cells(pos):
            return int((pos + 80) / 160)
            
        self.x = convert_to_cells(x_pos)
        self.y = convert_to_cells(y_pos)
        return self
    
    def get_object_summary(self):
        return { 
            "id": self.id,
            "x_cell": self.x,
            "y_cell": self.y,
            "flag": self.flag,
            "child_id": self.child_id,
            "child_flags": self.child_flags,
            "link_id": self.link_id,
            "extended_data": self.extended_data,
        }
    
    def is_superball(self):
        def is_flag_superball(flag):
            flag_binary = bin(flag)

            out = True
            for bit in Object.SUPERBALL_BIT_POSITION:
                if flag_binary[-bit] == '0':
                    out = False
                    break
                
            return out
        
        out = False
        if self.id == 34:
            out = is_flag_superball(self.flag)

        elif self.id in Object.SUPERBALL_CONTAINER_IDS and self.child_id == 34:
            out = is_flag_superball(self.child_flags)
                        
        return out
            

class CourseArea:
    coordinate_factor = 0.0075
    
    def __init__(self, data, area_offset):
        coordinate_factor = 0.0075
        self.object_count = int.from_bytes(seek_get(data, area_offset + 0x1C, 0x4), byteorder='little')
        
        # Objects
        self.objects = []
                
        object_offset = area_offset + 0x48
        for i in range(self.object_count):
                 
            object_id = int.from_bytes(seek_get(data, object_offset + 0x18, 0x2), byteorder='little')
            object_flag = int.from_bytes(seek_get(data, object_offset + 0xC, 0x4), byteorder='little')
                    
            child_id = int.from_bytes(seek_get(data, object_offset + 0x1A, 0x2), byteorder='little')
            child_flags = int.from_bytes(seek_get(data, object_offset + 0x10, 0x4), byteorder='little')
            
            x_coord = int.from_bytes(seek_get(data, object_offset + 0x0, 0x4), byteorder='little')
            y_coord = int.from_bytes(seek_get(data, object_offset + 0x4, 0x4), byteorder='little')
            
            link_id = int.from_bytes(seek_get(data, object_offset + 0x1C, 0x2), byteorder='little')
            
            extended_data = int.from_bytes(seek_get(data, object_offset + 0x14, 0x4), byteorder='little')

            # Builder because I can
            test_object = Object() \
                .set_id(object_id) \
                .set_flag(object_flag) \
                .set_child_id(child_id) \
                .set_child_flags(child_flags) \
                .set_coords(x_coord, y_coord) \
                .set_link_id(link_id) \
                .set_extended_data(extended_data)
                        
            self.objects.append(test_object)
                
            object_offset += 0x20
        

class Course:
    def __init__(self, data, difficulty, course_code):
        self.data = data
        
        self.superballs = []
        self.difficulty = difficulty
        self.course_code = course_code
        
        # Course Header
        self.course_style = str(seek_get(data, 0xF1, 0x2))
        self.course_description = seek_get(data, 0x136, 0xCA).decode('utf-16-le')
        self.course_name = seek_get(data, 0xF4, 0x42).decode('utf-16-le').split('\0')[0]
        
        # Course Area Main
        area_main_offset = 0x200
        self.area_main = CourseArea(data, area_main_offset)
                
        # Course Area Sub
        area_sub_offset = 0x2E0E0
        self.area_sub = CourseArea(data, area_sub_offset)
        
        for c_obj in [*self.area_main.objects, *self.area_sub.objects]:
            if c_obj.is_superball():
                self.superballs.append(c_obj)
                
        self.has_superball = len(self.superballs) > 0
                
    def __repr__(self):
        return json.dumps({
            'name': self.course_name,
            'course_code': self.course_code,
            'difficulty': self.difficulty,
            'superball_count': len(self.superballs),
            'superballs': [s.get_object_summary() for s in self.superballs],
        }, indent=4)
        
    def __str__(self):
        return f"{self.course_code}"
    
    @staticmethod
    def get_course_repr_keys():
        return ['name', 'course_code', 'difficulty', 'superball_count']
    
    # TODO: rename this to not be so close to api client method name
    def get_course_data(self):
        return {
            'name': self.course_name,
            'course_code': self.course_code,
            'difficulty': self.difficulty,
            'superball_count': len(self.superballs),
            'played': 0,
        }
    
    def get_superballs(self):
        return {
            'superballs': [s.get_object_summary() for s in self.superballs]
        }