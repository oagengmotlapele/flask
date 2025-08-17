from dataclasses import dataclass
@dataclass
class SortDataStructures:
    def sort_list_by_index(self,list_data_to_sort:list,index :int,reve:bool=True) -> list:
        return sorted(list_data_to_sort, key=lambda x: x[index], reverse=reve)

    def sort_dictionary_list_by_key(self, dictionary_to_sort  : list[dict] , key : str, sort_a:bool=False) -> list:
        return sorted(dictionary_to_sort, key=lambda x: x[key], reverse=sort_a)

    def sort_tuple_list_by_index(self, tuple_data_to_sort: list[tuple] ,index :int,reve:bool=True) -> tuple :
        return sorted(tuple_data_to_sort, key=lambda x: x[index], reverse=reve)