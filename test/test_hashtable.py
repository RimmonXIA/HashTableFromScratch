from hashtable import HashTable
import pytest
from pytest_unordered import unordered

@pytest.fixture    
def hash_table():
    sample_data = HashTable(capacity=100)
    sample_data["hola"] = "hello"
    sample_data[98.6] = 37
    sample_data[False] = True
    return sample_data

def test_should_create_hashtable():
    assert HashTable(capacity=100) is not None

def test_should_report_capacity_of_empty_hash_table():
    assert HashTable(capacity=100).capacity == 100

def test_should_report_capacity(hash_table):
    assert hash_table.capacity == 100

def test_should_create_empty_pair_slots():
    assert HashTable(capacity=3)._slots == [None] * 3
    
def test_should_insert_key_value_pairs():
    # Given
    hash_table = HashTable(capacity=100)
    
    # When
    hash_table['hola'] = "hello"
    hash_table[98.6] = 37
    hash_table[False] = True
    
    # Then
    assert ("hola", "hello") in hash_table.pairs
    assert (98.6, 37) in hash_table.pairs
    assert (False, True) in hash_table.pairs
    assert len(hash_table) == 3

@pytest.mark.skip
def test_should_not_shrink_when_removing_elements():
    pass

def test_should_not_contain_none_value_when_created():
    assert None not in HashTable(capacity=100).values

def test_should_insert_none_value():
    hash_table = HashTable(capacity=100)
    hash_table["key"] = None
    assert ("key", None) in hash_table.pairs

def test_should_find_value_by_key(hash_table):
    assert hash_table["hola"] == "hello"
    assert hash_table[98.6] == 37
    assert hash_table[False] == True

def test_should_raise_error_on_missing_key():
    hash_table = HashTable(capacity=100)
    with pytest.raises(KeyError) as exception_info:
        hash_table["missing_key"]
    assert exception_info.value.args[0] == "missing_key"

def test_should_find_key(hash_table):
    assert "hola" in hash_table

def test_should_not_find_key(hash_table):
    assert "missing_key" not in hash_table
    
def test_should_get_value(hash_table):
    assert hash_table.get("hola") == "hello"

def test_should_get_none_when_missing_key(hash_table):
    assert hash_table.get("missing_key") == None

def test_should_get_default_value_when_missing_key(hash_table):
    assert hash_table.get("missing_key", "default") == "default"

def test_should_get_value_with_default(hash_table):
    assert hash_table.get("hola", "default") == "hello"
    
def test_should_delete_key_value_pair(hash_table):
    assert ("hola", "hello") in hash_table.pairs
    assert "hola" in hash_table
    assert len(hash_table) == 3
        
    del hash_table["hola"]
    
    assert ("hola", "hello") not in hash_table.pairs
    assert "hola" not in hash_table
    assert len(hash_table) == 2

def test_should_raise_key_error_when_delete(hash_table):
    with pytest.raises(KeyError) as exception_info:
        del hash_table["missing_key"]
    assert exception_info.value.args[0] == "missing_key"
    
def test_should_update_value(hash_table):
    assert hash_table["hola"] == "hello"
    
    hash_table["hola"] = "hallo"
    
    assert hash_table["hola"] == "hallo"
    assert hash_table[98.6] == 37
    assert hash_table[False] == True
    assert len(hash_table) == 3
    
def test_should_return_pairs(hash_table):
    assert hash_table.pairs == {
        ("hola", "hello"),
        (98.6, 37),
        (False, True)
    }

def test_should_return_copy_of_pairs(hash_table):
    # Whenever you request the key-value pairs from a hash table, 
    #   you expect to get a brand-new object with a unique identity.
    assert hash_table.pairs is not hash_table.pairs
    
def test_should_not_include_blank_pairs(hash_table):
    assert None not in hash_table.pairs

def test_should_get_pairs_of_empty_hash_table():
    assert HashTable(capacity=100).pairs == set()

def test_should_return_duplicate_values():
    hash_table = HashTable(capacity=100)
    hash_table["Alice"] = 24
    hash_table["Bob"] = 42
    hash_table["Joe"] = 42
    assert [24, 42, 42] == sorted(hash_table.values)

def test_should_get_values(hash_table):
    assert unordered(hash_table.values) == ["hello", 37, True]

def test_should_get_values_of_empty_hash_table():
    assert HashTable(capacity=100).values == []

def test_should_return_copy_of_values(hash_table):
    assert hash_table.values is not hash_table.values

def test_should_get_keys(hash_table):
    assert hash_table.keys == {"hola", 98.6, False}

def test_should_get_keys_of_empty_hash_table():
    assert HashTable(capacity=100).keys == set()

def test_should_return_copy_of_keys(hash_table):
    assert hash_table.keys is not hash_table.keys

def test_should_convert_to_dict(hash_table):
    dictionary = dict(hash_table.pairs)
    assert set(dictionary.items()) == hash_table.pairs
    assert set(dictionary.keys()) == hash_table.keys
    assert list(dictionary.values()) == unordered(hash_table.values)
    
def test_should_report_length_of_empty_hash_table():
    assert len(HashTable(capacity=100)) == 0

def test_should_report_length(hash_table):
    assert len(hash_table) == 3

def test_should_not_create_hashtable_with_zero_capacity():
    with pytest.raises(ValueError):
        HashTable(capacity=0)

def test_should_not_create_hashtable_with_negative_capacity():
    with pytest.raises(ValueError):
        HashTable(capacity=-100)
        
def test_should_iterate_over_values(hash_table):
    for value in hash_table.values:
        assert value in ("hello", 37, True)

def test_should_iterate_over_keys(hash_table):
    for key in hash_table.keys:
        assert key in ("hola", 98.6, False)

def test_should_iterate_over_items(hash_table):
    for key, value in hash_table.pairs:
        assert key in ("hola", 98.6, False)
        assert value in ("hello", 37, True)

def test_should_iterate_over_instance(hash_table):
    for key in hash_table:
        assert key in ("hola", 98.6, False)

def test_should_use_dict_literal_for_str(hash_table):
    assert str(hash_table) in {
        "{'hola': 'hello', 98.6: 37, False: True}",
        "{'hola': 'hello', False: True, 98.6: 37}",
        "{98.6: 37, 'hola': 'hello', False: True}",
        "{98.6: 37, False: True, 'hola': 'hello'}",
        "{False: True, 'hola': 'hello', 98.6: 37}",
        "{False: True, 98.6: 37, 'hola': 'hello'}",
    }

def test_should_create_hashtable_from_dict():
    dictionary = {"hola": "hello", 98.6: 37, False: True}
    
    hash_table = HashTable.from_dict(dictionary)
    
    assert hash_table.capacity == len(dictionary) * 10
    assert hash_table.keys == set(dictionary.keys())
    assert unordered(hash_table.values) == list(dictionary.values())
    assert hash_table.pairs == set(dictionary.items())
    
def test_should_create_hashtable_from_dict_with_custom_capacity():
    dictionary = {"hola": "hello", 98.6: 37, False: True}
    
    hash_table = HashTable.from_dict(dictionary, capacity=100)
    
    assert hash_table.capacity == 100
    assert hash_table.keys == set(dictionary.keys())
    assert unordered(hash_table.values) == list(dictionary.values())
    assert hash_table.pairs == set(dictionary.items())

def test_should_have_canonical_string_representation(hash_table):
    assert repr(hash_table) in {
        "HashTable.from_dict({'hola': 'hello', 98.6: 37, False: True})",
        "HashTable.from_dict({'hola': 'hello', False: True, 98.6: 37})",
        "HashTable.from_dict({98.6: 37, 'hola': 'hello', False: True})",
        "HashTable.from_dict({98.6: 37, False: True, 'hola': 'hello'})",
        "HashTable.from_dict({False: True, 'hola': 'hello', 98.6: 37})",
        "HashTable.from_dict({False: True, 98.6: 37, 'hola': 'hello'})",
    }