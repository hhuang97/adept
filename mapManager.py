import os
from multiprocessing import Process, Queue
from threading import Thread

from buffalo import utils

class MapManager:
    """
    Manages chunks and map loading
    """

    BASE_PATH    = ["maps"] # BASE_PATH is a list version of the base path in
                            # which MapManager will search for chunks. For example,
                            # if the base path should be maps/otherfolder/ then
                            # BASE_PATH should equal ["maps", "otherfolder"]
    maps          = []      # Maps is a list of all Map's found in within BASE_PATH
    activeMap     = None    # activeMap is the active map // lol

    loaded_chunks = dict()
    lru_chunks    = dict()  # least recently used chunks

    @staticmethod
    def loadMaps():
        """
        loadMaps loads all the maps that are checked in the plugins manager file
        """
        for name in PluginManager.mapNames:
            MapManager.loadMap(name)
        MapManager.maps.sort(key=lambda m: m.precedence)
        MapManager.activeMap = MapManager.maps[0]
        # THIS LINE IS REALLY IMPORTANT
        MapManager.soft_load_reader_queue = Queue()
        MapManager.soft_load_writer_queue = Queue()
        MapManager.soft_load_render_queue = Queue()

    @staticmethod
    def loadMap( map_name ):
        """
        loadMap takes one string map_name and attempts to load the corresponding map
        """
        CHUNK_PATH_LIST = MapManager.BASE_PATH + [map_name, "chunks"]
        MapManager.maps.append(Map(map_name, CHUNK_PATH_LIST))

    @staticmethod
    def get_chunk_coords(world_pos):
        return (
            int(world_pos[0] / (Chunk.CHUNK_WIDTH * Chunk.TILE_SIZE)),
            int(world_pos[1] / (Chunk.CHUNK_HEIGHT * Chunk.TILE_SIZE)),
        )

    @staticmethod
    def hard_load(world_pos):
        x, y = MapManager.get_chunk_coords(world_pos)
        for j in range(y - 2, y + 3):
            for i in range(x - 2, x + 3):
                if (i, j) not in MapManager.loaded_chunks.keys():
                    MapManager.loaded_chunks[(i, j)] = Chunk(i, j)
                    MapManager.lru_chunks[(i, j)] = 2
        if hasattr(MapManager, 'soft_load_reader_process'):
            MapManager.soft_load_reader_process.join()
        if hasattr(MapManager, 'soft_load_render_thread'):
            MapManager.soft_load_render_thread.join()
        MapManager.soft_load_reader_process = MapManager.get_soft_load_reader_process()
        MapManager.soft_load_reader_process.start()
        MapManager.soft_load_reader_queue.put(world_pos)
        MapManager.soft_load_reader_queue.put("DONE")
#        MapManager.soft_load_render_thread = MapManager.get_soft_load_render_thread(world_pos)
#        MapManager.soft_load_render_thread.start()

    @staticmethod
    def soft_load(world_pos):
        x, y = MapManager.get_chunk_coords(world_pos)
        for j in range(y - 4, y + 5): # sides
            for i in range(x - 4, x - 2) + range(x + 3, x + 5):
                #MapManager.loaded_chunks[(i, j)] = Chunk(i, j)
                if (i, j) not in MapManager.loaded_chunks:
                    package = ((x, y), (i, j), Chunk(i, j, from_other_process=False))
                    MapManager.soft_load_writer_queue.put(package)
        for j in range(y - 4, y - 2) + range(y + 3, y + 5): # top and bottom
            for i in range(x - 4, x + 5): 
                #MapManager.loaded_chunks[(i, j)] = Chunk(i, j)
                if (i, j) not in MapManager.loaded_chunks:
                    package = ((x, y), (i, j), Chunk(i, j, from_other_process=False))
                    MapManager.soft_load_writer_queue.put(package)

    @staticmethod
    def offload_old_chunks():
        # This method goes through the lru_chunks dictionary
        # and determines which chunks don't need to be in memory
        # based on when they were last used relative to other chunks
        for key in MapManager.lru_chunks.keys():
            if MapManager.lru_chunks[key] == 0:
                if key in MapManager.loaded_chunks.keys():
                    del MapManager.loaded_chunks[key]
                del MapManger.lru_chunks[key]

    @staticmethod
    def soft_load_reader():
        while True:
            world_pos = MapManager.soft_load_reader_queue.get()
            if world_pos == "DONE":
                break
            else:
                MapManager.soft_load(world_pos)

    @staticmethod
    def soft_load_writer():
        if MapManager.soft_load_writer_queue.empty():
            return
        package = MapManager.soft_load_writer_queue.get()
        coords, pos, chunk = package
        chunk.create_and_render_surface()
        #chunk.create_surface()
        MapManager.loaded_chunks[pos] = chunk
        if pos in MapManager.lru_chunks.keys():
            MapManager.lru_chunks[pos] = 1
        else:
            MapManager.lru_chunks[pos] = 1
        x, y = coords
        for i, j in MapManager.loaded_chunks.keys():
            if i < x - 4 or i > x + 4 or j < y - 4 or j > y + 4:
                # these  are really far away chunks that can be offloaded if necessary
                MapManager.lru_chunks[i, j] = 0

    @staticmethod
    def soft_load_render(world_pos):
        x, y = MapManager.get_chunk_coords(world_pos)
        for j in range(y - 4, y - 2) + range(y + 3, y + 5):
            for i in range(x - 4, x - 2) + range(x + 3, x + 5):
                if (i, j) in MapManager.loaded_chunks.keys():
                    MapManager.loaded_chunks[(i, j)].create_and_render_surface()
        
    @staticmethod
    def get_soft_load_render_thread(world_pos):
        soft_load_render_thread = Thread(target=MapManager.soft_load_render, args=((world_pos),))
        soft_load_render_thread.daemon = True
        return soft_load_render_thread

    @staticmethod
    def get_soft_load_reader_process():
        soft_load_reader_process = Process(target=MapManager.soft_load_reader)
        soft_load_reader_process.daemon = True
        return soft_load_reader_process

from Map import Map
from pluginManager import PluginManager
from chunk import Chunk
