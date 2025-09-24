# Import required libraries
import random  # For shuffling room order to add randomization
from typing import Dict, List, Tuple, Set, Optional  # Type hints for better code clarity
from collections import deque  # Double-ended queue for efficient queue operations

class RoomLayoutGenerator:
    def __init__(self, rooms: Dict[str, List[str]], start_room: str, start_exits: List[str]):
        """
        Initialize the layout generator.
        
        Args:
            rooms: Dictionary mapping room_id -> list of exit directions
            start_room: ID of the starting room
            start_exits: List of exits from the starting room (e.g., ["up", "left", "right"])
        """
        self.rooms = rooms
        self.start_room = start_room
        self.start_exits = start_exits
        
        # Direction mappings
        self.opposite_dirs = {
            "up": "down",
            "down": "up", 
            "left": "right",
            "right": "left"
        }
        
        # Position offsets for each direction
        self.dir_offsets = {
            "up": (0, 1),
            "down": (0, -1),
            "left": (-1, 0),
            "right": (1, 0)
        }
        
    def generate_layout(self, max_attempts: int = 100) -> Optional[Dict[Tuple[int, int], str]]:
        """
        Generate a valid room layout using backtracking.
        
        Returns:
            Dictionary mapping (x, y) positions to room IDs, or None if no solution found
        """
        for attempt in range(max_attempts):
            layout = self._attempt_layout()
            if layout:
                return layout
                
        print(f"Failed to generate layout after {max_attempts} attempts")
        return None
    
    def _attempt_layout(self) -> Optional[Dict[Tuple[int, int], str]]:
        """Single attempt to generate a layout using backtracking."""
        # Start with the starting room at origin
        layout = {(0, 0): self.start_room}
        used_rooms = {self.start_room}
        available_rooms = [room_id for room_id in self.rooms.keys() if room_id != self.start_room]
        
        # Queue of positions that need connections: (position, required_entrance_direction)
        connection_queue = deque()
        
        # Add initial connections from start room
        for exit_dir in self.start_exits:
            new_pos = self._get_adjacent_position((0, 0), exit_dir)
            required_entrance = self.opposite_dirs[exit_dir]
            connection_queue.append((new_pos, required_entrance))
        
        return self._backtrack_layout(layout, used_rooms, available_rooms, connection_queue)
    
    def _backtrack_layout(self, layout: Dict[Tuple[int, int], str], 
                         used_rooms: Set[str], available_rooms: List[str],
                         connection_queue: deque) -> Optional[Dict[Tuple[int, int], str]]:
        """
        Recursive backtracking to place rooms.
        """
        if not connection_queue:
            return layout  # Successfully placed all required connections
            
        # Get next position that needs a room
        pos, required_entrance = connection_queue.popleft()
        
        # Skip if position is already occupied
        if pos in layout:
            return self._backtrack_layout(layout, used_rooms, available_rooms, connection_queue)
        
        # Try each available room at this position
        random.shuffle(available_rooms)  # Add randomization
        
        for i, room_id in enumerate(available_rooms):
            room_exits = self.rooms[room_id]
            
            # Check if this room can accept the required entrance
            if required_entrance not in room_exits:
                continue
                
            # Check if placing this room would create conflicts
            if not self._is_valid_placement(layout, pos, room_id, room_exits):
                continue
                
            # Place the room
            new_layout = layout.copy()
            new_layout[pos] = room_id
            new_used_rooms = used_rooms.copy()
            new_used_rooms.add(room_id)
            new_available_rooms = available_rooms[:i] + available_rooms[i+1:]
            new_queue = connection_queue.copy()
            
            # Add new required connections from this room's other exits
            for exit_dir in room_exits:
                if exit_dir != required_entrance:  # Don't re-add the entrance we just used
                    new_pos = self._get_adjacent_position(pos, exit_dir)
                    if new_pos not in new_layout:  # Only add if position is empty
                        required_new_entrance = self.opposite_dirs[exit_dir]
                        new_queue.append((new_pos, required_new_entrance))
            
            # Recursively try to complete the layout
            result = self._backtrack_layout(new_layout, new_used_rooms, 
                                          new_available_rooms, new_queue)
            if result:
                return result
        
        # No valid room found for this position, backtrack
        connection_queue.appendleft((pos, required_entrance))
        return None
    
    def _is_valid_placement(self, layout: Dict[Tuple[int, int], str], 
                          pos: Tuple[int, int], room_id: str, 
                          room_exits: List[str]) -> bool:
        """
        Check if placing a room at a position would create any conflicts.
        """
        for exit_dir in room_exits:
            adjacent_pos = self._get_adjacent_position(pos, exit_dir)
            
            # If there's already a room at the adjacent position
            if adjacent_pos in layout:
                adjacent_room_id = layout[adjacent_pos]
                adjacent_exits = self.rooms[adjacent_room_id]
                required_entrance = self.opposite_dirs[exit_dir]
                
                # The adjacent room must have a matching entrance
                if required_entrance not in adjacent_exits:
                    return False
                    
        return True
    
    def _get_adjacent_position(self, pos: Tuple[int, int], direction: str) -> Tuple[int, int]:
        """Get the position adjacent to pos in the given direction."""
        offset = self.dir_offsets[direction]
        return (pos[0] + offset[0], pos[1] + offset[1])
    
    def print_layout(self, layout: Dict[Tuple[int, int], str]):
        """Print a visual representation of the layout."""
        if not layout:
            print("No layout generated")
            return
            
        # Find bounds
        min_x = min(pos[0] for pos in layout.keys())
        max_x = max(pos[0] for pos in layout.keys())
        min_y = min(pos[1] for pos in layout.keys())
        max_y = max(pos[1] for pos in layout.keys())
        
        print("\nGenerated Layout:")
        print("=" * 50)
        
        # Print from top to bottom (high y to low y)
        for y in range(max_y, min_y - 1, -1):
            row = ""
            for x in range(min_x, max_x + 1):
                if (x, y) in layout:
                    room_id = layout[(x, y)]
                    exits = self.rooms[room_id]
                    
                    # Show room with its exits
                    exit_str = "".join([d[0].upper() for d in exits])  # First letter of each exit
                    row += f"{room_id}({exit_str})".ljust(12)
                else:
                    row += "     ·      "
            print(f"y={y:2d} | {row}")
        
        # Print x-axis labels
        x_labels = "     "
        for x in range(min_x, max_x + 1):
            x_labels += f"x={x}".ljust(12)
        print(x_labels)


# Example usage and testing
def main():
    # Example room definitions
    rooms = {
        "1_3": ["right", "up"],
        "2_1": ["left", "down"],
        "3_2": ["up", "down", "left"],
        "4_1": ["right"],
        "5_2": ["left", "right"],
        "6_1": ["down"],
        "7_3": ["up", "left", "right"],
        "8_1": ["up"],
        "9_2": ["down", "right"],
        "10_1": ["left"]
    }
    
    # Starting room configuration
    start_room = "start"
    start_exits = ["up", "left", "right"]
    
    # Add start room to rooms dict
    rooms[start_room] = start_exits
    
    # Generate layout
    generator = RoomLayoutGenerator(rooms, start_room, start_exits)
    layout = generator.generate_layout(max_attempts=50)
    
    if layout:
        generator.print_layout(layout)
        
        # Verify the layout is valid
        print("\nValidation:")
        is_valid = validate_layout(layout, rooms, generator)
        print(f"Layout is valid: {is_valid}")
    else:
        print("Could not generate a valid layout with the given rooms.")


def validate_layout(layout: Dict[Tuple[int, int], str], 
                   rooms: Dict[str, List[str]], 
                   generator: RoomLayoutGenerator) -> bool:
    """Validate that a layout has proper door connections."""
    for pos, room_id in layout.items():
        room_exits = rooms[room_id]
        
        for exit_dir in room_exits:
            adjacent_pos = generator._get_adjacent_position(pos, exit_dir)
            
            # If there's a room at the adjacent position
            if adjacent_pos in layout:
                adjacent_room_id = layout[adjacent_pos]
                adjacent_exits = rooms[adjacent_room_id]
                required_entrance = generator.opposite_dirs[exit_dir]
                
                # Check if the adjacent room has the matching entrance
                if required_entrance not in adjacent_exits:
                    print(f"Validation failed: Room {room_id} at {pos} has exit {exit_dir}, "
                          f"but room {adjacent_room_id} at {adjacent_pos} doesn't have entrance {required_entrance}")
                    return False
                    
    return True


if __name__ == "__main__":
    main()