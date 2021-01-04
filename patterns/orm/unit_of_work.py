import threading


class UnitOfWork:
    current = threading.local()

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def clean(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def set_mapper_registry(self, MapperRegistry):
        self.MapperRegistry = MapperRegistry
        self.set_id_map()

    def set_id_map(self):
        self.id_map = dict.fromkeys(self.MapperRegistry.mappers.keys())
        print("----------------------")
        self.fill_id_map()
        print("---- ID MAP ---- \n", self.id_map)

    def register_new(self, object_):
        print('object_', object_)
        self.new_objects.append(object_)

    def register_updated(self, object_):
        self.dirty_objects.append(object_)

    def register_removed(self, object_):
        self.removed_objects.append(object_)

    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_removed()
        self.clean()

    def insert_new(self):
        for obj in self.new_objects:
            mapper = self.MapperRegistry.get_mapper(obj)
            mapper.insert(obj)
            id_ = mapper.get_last_id()
            self.get_map_by_registry(mapper)[id_] = obj
            obj.id = id_
            print('---------insert--------\n', self.get_map_by_registry(mapper), self.get_map_by_registry(mapper)[id_])
            print('--------AFTER_INSERT_ID_MAP----------\n', self.id_map)

    def update_dirty(self):
        for obj in self.dirty_objects:
            mapper = self.MapperRegistry.get_mapper(obj)
            mapper.update(obj)
            self.get_map_by_registry(mapper)[obj.id] = obj

    def delete_removed(self):
        for obj in self.removed_objects:
            mapper = self.MapperRegistry.get_mapper(obj)
            mapper.delete(obj)
            self.get_map_by_registry(mapper).pop(obj.id)

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work

    def fill_id_map(self):
        for map_name in self.id_map:
            objs = self.MapperRegistry.get_curr_mapper(map_name).all()
            if self.id_map[map_name] is None:
                self.id_map[map_name] = {}
            for obj in objs:
                self.id_map[map_name][obj.id] = obj

    def get_id_map(self, mapper_name) -> dict:
        print(mapper_name)
        return self.id_map[mapper_name]

    def all(self, mapper_name) -> list:
        return list(self.get_id_map(mapper_name).values())

    def get_by_id(self, mapper_name, id: int):
        id_map_ = self.get_id_map(mapper_name)
        res = id_map_.get(id)
        if not res:
            res = self.MapperRegistry.get_curr_mapper(mapper_name).get_by_id(id)
            id_map_[res.id] = res
        return res

    def get_map_by_registry(self, registry) -> dict:
        print('registry', registry)
        return self.get_id_map(self.MapperRegistry.get_mapper_name(registry))


class DomainObject:

    def mark_new(self):
        UnitOfWork.get_current().register_new(self)

    def mark_dirty(self):
        UnitOfWork.get_current().register_dirty(self)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)
