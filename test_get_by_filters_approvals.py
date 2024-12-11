import pytest
import random

from utils.indexer_endpoints import BASE_URL_IDX
from utils.fetch import fetch_get
from assertpy import assert_that
from utils.random_data_limit_offset import get_random_limit


@pytest.fixture()
def extract_values_from_response(request):
    """
    Extract specific values from the response.
    """
    url = request.param  # Access the parameterized value
    resp, body = fetch_get(url, params=[])

    # Extract relevant fields from the response
    extracted_values = [
        (
            int(value["blockNumber"]),
            int(value["blockTs"]),
            int(value["value"]),
            str(value["owner"]),
            str(value["spender"]),
            str(value["txHash"]),
            int(value["indexedAt"]),
            int(value["logIndex"]),
        )
        for value in body["values"]
    ]

    # Get a random sample of 3 values, ensuring there are at least 1 values to sample
    if len(extracted_values) < 1:
        raise ValueError("Not enough values in the response to extract a sample of 1.")

    random_values = random.choice(extracted_values)
    return url, random_values


@pytest.mark.parametrize("extract_values_from_response", [f"{BASE_URL_IDX}api/v1/events/GetByFiltersApprovals"],
                         indirect=True)
def test_value_filter(extract_values_from_response):
    url, random_values = extract_values_from_response
    value = random_values[2]
    resp, body = fetch_get(url, params=[f'value={value}'])

    print(f"Status code: {resp.status_code}")
    assert resp.status_code == 200, f"Expected status code 200, but got {resp.status_code} instead."

    objs = body['values']
    for obj in objs:
        print(f"value: {int(obj['value'])}")
        assert_that(int(obj['value'])).is_equal_to(value).described_as(
            f"The value filter is not working correctly."
            f"Expected Value: '{value}' in the params, but got Value: '{int(obj['value'])}' in the response objects.")
        assert_that(len(objs)).is_equal_to(int(body['total'])).described_as(
            f"Expected 'total' in response body ({body['total']}) to match the length of 'objs' ({len(objs)})")


@pytest.mark.parametrize("extract_values_from_response", [f"{BASE_URL_IDX}api/v1/events/GetByFiltersApprovals"],
                         indirect=True)  # The indirect=True argument tells pytest to pass these values to the fixture
# through the request object instead of directly to the test function.
def test_value_gt_filter(extract_values_from_response):
    url, random_values = extract_values_from_response
    value = random_values[2]
    resp, body = fetch_get(url, params=[f'valueFilterGt={value}'])

    print(f"Status code: {resp.status_code}")
    assert resp.status_code == 200

    objs = body['values']
    for obj in objs:
        print(f"value: {int(obj['value'])}")
        assert_that(int(obj['value'])).is_greater_than(value)


@pytest.mark.parametrize("extract_values_from_response", [f"{BASE_URL_IDX}api/v1/events/GetByFiltersApprovals"],
                         indirect=True)
def test_value_ge_filter(extract_values_from_response):
    url, random_values = extract_values_from_response
    value = random_values[2]
    resp, body = fetch_get(url, params=[f'valueFilterGe={value}'])

    print(f"Status code: {resp.status_code}")
    assert resp.status_code == 200, f"Expected status code 200, but got {resp.status_code} instead."

    objs = body['values']
    for obj in objs:
        print(f"value: {int(obj['value'])}")
        assert_that(int(obj['value'])).is_greater_than_or_equal_to(value)


@pytest.mark.parametrize("extract_values_from_response", [f"{BASE_URL_IDX}api/v1/events/GetByFiltersApprovals"],
                         indirect=True)
def test_value_lt_filter(extract_values_from_response):
    url, random_values = extract_values_from_response
    value = random_values[2]
    resp, body = fetch_get(url, params=[f'valueFilterLt={value}'])

    print(f"Status code: {resp.status_code}")
    assert resp.status_code == 200, f"Expected status code 200, but got {resp.status_code} instead."

    objs = body['values']
    for obj in objs:
        print(f"value: {int(obj['value'])}")
        assert_that(int(obj['value'])).is_less_than(value)


@pytest.mark.parametrize("extract_values_from_response", [f"{BASE_URL_IDX}api/v1/events/GetByFiltersApprovals"],
                         indirect=True)
def test_value_le_filter(extract_values_from_response):
    url, random_values = extract_values_from_response
    value = random_values[2]
    resp, body = fetch_get(url, params=[f'valueFilterLe={value}'])

    print(f"Status code: {resp.status_code}")
    assert resp.status_code == 200, f"Expected status code 200, but got {resp.status_code} instead."

    objs = body['values']
    for obj in objs:
        print(f"value: {int(obj['value'])}")
        assert_that(int(obj['value'])).is_less_than_or_equal_to(value)


@pytest.mark.parametrize("extract_values_from_response", [f"{BASE_URL_IDX}api/v1/events/GetByFiltersApprovals"],
                         indirect=True)
def test_value_sort_asc(extract_values_from_response):
    url, _ = extract_values_from_response
    resp, body = fetch_get(url, params=['valueSortAsc=true'])

    print(f"Status code: {resp.status_code}")
    assert resp.status_code == 200, f"Expected status code 200, but got {resp.status_code} instead."

    objs = body['values']
    # Convert all values to integers
    values = [int(obj['value']) for obj in objs]

    # Check if values are sorted in ascending order
    for i in range(len(values) - 1):
        assert values[i] <= values[i + 1], f"Values are not sorted in ascending order: {values}"

    print("All values are sorted in ascending order.")


@pytest.mark.parametrize("extract_values_from_response", [f"{BASE_URL_IDX}api/v1/events/GetByFiltersApprovals"],
                         indirect=True)
def test_value_sort_desc(extract_values_from_response):
    url, _ = extract_values_from_response
    resp, body = fetch_get(url, params=['valueSortDesc=true'])

    print(f"Status code: {resp.status_code}")
    assert resp.status_code == 200, f"Expected status code 200, but got {resp.status_code} instead."

    objs = body['values']
    # Convert all values to integers
    values = [int(obj['value']) for obj in objs]

    # Check if values are sorted in descending order
    for i in range(len(values) - 1):
        assert values[i] >= values[i + 1], f"Values are not sorted in descending order: {values}"

    print("All values are sorted in descending order.")


@pytest.mark.parametrize("extract_values_from_response", [f"{BASE_URL_IDX}api/v1/events/GetByFiltersApprovals"],
                         indirect=True)
def test_block_number_filter(extract_values_from_response):
    url, random_values = extract_values_from_response
    blockNumber = random_values[0]
    resp, body = fetch_get(url, params=[f'blockNumber={blockNumber}'])

    print(f"Status code: {resp.status_code}")
    assert resp.status_code == 200, f"Expected status code 200, but got {resp.status_code} instead."

    objs = body['values']
    for obj in objs:
        print(f"blockNumber: {int(obj['blockNumber'])}")
        assert_that(int(obj['blockNumber'])).is_equal_to(blockNumber).described_as(
            f"The blockNumber filter is not working correctly."
            f"Expected blockNumber: '{blockNumber}' in the params, but got blockNumber: '{int(obj['blockNumber'])}'"
            f" in the response objects.")
        assert_that(len(objs)).is_equal_to(int(body['total'])).described_as(
            f"Expected 'total' in response body ({body['total']}) to match the length of 'objs' ({len(objs)})")


@pytest.mark.parametrize("extract_values_from_response", [f"{BASE_URL_IDX}api/v1/events/GetByFiltersApprovals"],
                         indirect=True)
def test_block_number_value_ge(extract_values_from_response):
    url, random_values = extract_values_from_response
    blockNumber = random_values[0]
    resp, body = fetch_get(url, params=[f'blockNumberFilterGe={blockNumber}'])

    print(f"Status code: {resp.status_code}")
    assert resp.status_code == 200, f"Expected status code 200, but got {resp.status_code} instead."

    objs = body['values']
    for obj in objs:
        print(f"blockNumber: {int(obj['blockNumber'])}")
        assert_that(int(obj['blockNumber'])).is_greater_than_or_equal_to(blockNumber)


@pytest.mark.parametrize("extract_values_from_response", [f"{BASE_URL_IDX}api/v1/events/GetByFiltersApprovals"],
                         indirect=True)
def test_block_number_value_lt(extract_values_from_response):
    url, random_values = extract_values_from_response
    blockNumber = random_values[0]
    resp, body = fetch_get(url, params=[f'blockNumberFilterLt={blockNumber}'])

    print(f"Status code: {resp.status_code}")
    assert resp.status_code == 200, f"Expected status code 200, but got {resp.status_code} instead."

    objs = body['values']
    for obj in objs:
        print(f"blockNumber: {int(obj['blockNumber'])}")
        assert_that(int(obj['blockNumber'])).is_less_than(blockNumber)


@pytest.mark.parametrize("extract_values_from_response", [f"{BASE_URL_IDX}api/v1/events/GetByFiltersApprovals"],
                         indirect=True)
def test_block_number_sort_asc(extract_values_from_response):
    url, _ = extract_values_from_response
    resp, body = fetch_get(url, params=['blockNumberSortAsc=true'])

    print(f"Status code: {resp.status_code}")
    assert resp.status_code == 200, f"Expected status code 200, but got {resp.status_code} instead."

    objs = body['values']
    # Convert all values to integers
    values = [int(obj['blockNumber']) for obj in objs]

    # Check if values are sorted in ascending order
    for i in range(len(values) - 1):
        print(f"blockNumber: {values[i]}")
        assert values[i] <= values[i + 1], f"Values are not sorted in ascending order: {values}"

    print("All values are sorted in ascending order.")


@pytest.mark.parametrize("extract_values_from_response", [f"{BASE_URL_IDX}api/v1/events/GetByFiltersApprovals"],
                         indirect=True)
def test_block_ts_filter(extract_values_from_response):
    url, random_values = extract_values_from_response
    blockTs = random_values[1]
    resp, body = fetch_get(url, params=[f'blockTs={blockTs}'])

    print(f"Status code: {resp.status_code}")
    assert resp.status_code == 200, f"Expected status code 200, but got {resp.status_code} instead."

    objs = body['values']
    for obj in objs:
        print(f"blockTs: {obj['blockTs']}")
        assert_that(obj['blockTs']).is_equal_to(blockTs).described_as(
            f"The blockTs filter is not working correctly."
            f"Expected blockTs: '{blockTs}' in the params, but got blockTs: '{obj['blockTs']}'"
            f" in the response objects.")
        assert_that(len(objs)).is_equal_to(int(body['total'])).described_as(
            f"Expected 'total' in response body ({body['total']}) to match the length of 'objs' ({len(objs)})")


@pytest.mark.parametrize("extract_values_from_response", [f"{BASE_URL_IDX}api/v1/events/GetByFiltersApprovals"],
                         indirect=True)
def test_block_ts_value_ge(extract_values_from_response):
    url, random_values = extract_values_from_response
    blockTs = random_values[1]
    resp, body = fetch_get(url, params=[f'blockTsFilterGe={blockTs}'])
    objs = body['values']
    for obj in objs:
        print(f"blockTs: {obj['blockTs']}")
        assert_that(obj['blockTs']).is_greater_than_or_equal_to(blockTs)


@pytest.mark.parametrize("extract_values_from_response", [f"{BASE_URL_IDX}api/v1/events/GetByFiltersApprovals"],
                         indirect=True)
def test_block_ts_value_lt(extract_values_from_response):
    url, random_values = extract_values_from_response
    blockTs = random_values[1]
    resp, body = fetch_get(url, params=[f'blockTsFilterLt={blockTs}'])

    print(f"Status code: {resp.status_code}")
    assert resp.status_code == 200, f"Expected status code 200, but got {resp.status_code} instead."

    objs = body['values']
    for obj in objs:
        print(f"blockTs: {obj['blockTs']}")
        assert_that(obj['blockTs']).is_less_than(blockTs)


@pytest.mark.parametrize("extract_values_from_response", [f"{BASE_URL_IDX}api/v1/events/GetByFiltersApprovals"],
                         indirect=True)
def test_block_ts_sort_asc(extract_values_from_response):
    url, _ = extract_values_from_response
    resp, body = fetch_get(url, params=['blockTsSortAsc=true'])

    print(f"Status code: {resp.status_code}")
    assert resp.status_code == 200, f"Expected status code 200, but got {resp.status_code} instead."

    objs = body['values']
    # Convert all values to integers
    values = [int(obj['blockTs']) for obj in objs]

    # Check if values are sorted in ascending order
    for i in range(len(values) - 1):
        print(f"blockTs: {values[i]}")
        assert values[i] <= values[i + 1], f"blockTs values are not sorted in ascending order: {values}"

    print("All blockTs values are sorted in ascending order.")


@pytest.mark.parametrize("extract_values_from_response", [f"{BASE_URL_IDX}api/v1/events/GetByFiltersApprovals"],
                         indirect=True)
def test_block_ts_sort_desc(extract_values_from_response):
    url, _ = extract_values_from_response
    resp, body = fetch_get(url, params=['blockTsSortDesc=true'])

    print(f"Status code: {resp.status_code}")
    assert resp.status_code == 200, f"Expected status code 200, but got {resp.status_code} instead."

    objs = body['values']

    # Convert all values to integers
    values = [int(obj['blockTs']) for obj in objs]

    # Check if values are sorted in descending order
    for i in range(len(values) - 1):
        print(f"blockTs: {values[i]}")
        assert values[i] >= values[i + 1], f"blockTs values are not sorted in descending order: {values}"

    print("All blockTs values are sorted in descending order.")


@pytest.mark.parametrize("extract_values_from_response", [f"{BASE_URL_IDX}api/v1/events/GetByFiltersApprovals"],
                         indirect=True)
def test_owner_value_filter(extract_values_from_response):
    url, random_values = extract_values_from_response
    owner = random_values[3]
    resp, body = fetch_get(url, params=[f'owner={owner}&limit=10000'])

    print(f"Status code: {resp.status_code}")
    assert resp.status_code == 200, f"Expected status code 200, but got {resp.status_code} instead."

    objs = body['values']
    for obj in objs:
        print(f"owner: {str(obj['owner'])}")
        assert_that(str(obj['owner'])).is_equal_to(owner).described_as(
            f"The owner address filter is not working correctly."
            f"Expected owner address '{owner}' in the params, but got '{str(obj['owner'])}' in the response objects.")
        assert_that(len(objs)).is_equal_to(int(body['total'])).described_as(
            f"Expected 'total' in response body ({body['total']}) to match the length of 'objs' ({len(objs)})")


@pytest.mark.parametrize("extract_values_from_response", [f"{BASE_URL_IDX}api/v1/events/GetByFiltersApprovals"],
                         indirect=True)
def test_owner_sort_asc(extract_values_from_response):
    url, _ = extract_values_from_response
    resp, body = fetch_get(url, params=['ownerSortAsc=true'])

    print(f"Status code: {resp.status_code}")
    assert resp.status_code == 200, f"Expected status code 200, but got {resp.status_code} instead."

    objs = body['values']
    # Create all owners' list values
    values = [obj['owner'] for obj in objs]

    # Verify if the list is sorted
    is_sorted = all(values[i] <= values[i + 1] for i in range(len(values) - 1))

    for owner in values:
        print(f"owner: {owner}")

    assert is_sorted, "Owners are not sorted in ascending order."
    print("All owner addresses are sorted in ascending order.")


@pytest.mark.parametrize("extract_values_from_response", [f"{BASE_URL_IDX}api/v1/events/GetByFiltersApprovals"],
                         indirect=True)
def test_owner_sort_desc(extract_values_from_response):
    url, _ = extract_values_from_response
    resp, body = fetch_get(url, params=['ownerSortDesc=true'])

    print(f"Status code: {resp.status_code}")
    assert resp.status_code == 200, f"Expected status code 200, but got {resp.status_code} instead."

    objs = body['values']
    # Create all owners' list values
    values = [obj['owner'] for obj in objs]

    # Verify if the list is sorted
    is_sorted = all(values[i] >= values[i + 1] for i in range(len(values) - 1))

    for owner in values:
        print(f"owner: {owner}")

    assert is_sorted, "Owners are not sorted in descending order."
    print("All owner addresses are sorted in descending order.")


@pytest.mark.parametrize("extract_values_from_response", [f"{BASE_URL_IDX}api/v1/events/GetByFiltersApprovals"],
                         indirect=True)
def test_spender_value_filter(extract_values_from_response):
    url, random_values = extract_values_from_response
    spender = random_values[4]
    resp, body = fetch_get(url, params=[f'spender={spender}&limit=10000'])

    print(f"Status code: {resp.status_code}")
    assert resp.status_code == 200, f"Expected status code 200, but got {resp.status_code} instead."

    objs = body['values']
    for obj in objs:
        print(f"spender: {str(obj['spender'])}")
        assert_that(str(obj['spender'])).is_equal_to(spender).described_as(
            f"The spender address filter is not working correctly."
            f"Expected spender address '{spender}' in the params, but got '{str(obj['spender'])}' in the response objects.")
        assert_that(len(objs)).is_equal_to(int(body['total'])).described_as(
            f"Expected 'total' in response body ({body['total']}) to match the length of 'objs' ({len(objs)})")


@pytest.mark.parametrize("extract_values_from_response", [f"{BASE_URL_IDX}api/v1/events/GetByFiltersApprovals"],
                         indirect=True)
def test_spender_sort_asc(extract_values_from_response):
    url, _ = extract_values_from_response
    resp, body = fetch_get(url, params=['spenderSortAsc=true'])

    print(f"Status code: {resp.status_code}")
    assert resp.status_code == 200, f"Expected status code 200, but got {resp.status_code} instead."

    objs = body['values']
    # Create all spenders' list values
    values = [obj['spender'] for obj in objs]

    # Verify if the list is sorted
    is_sorted = all(values[i] <= values[i + 1] for i in range(len(values) - 1))

    for spender in values:
        print(f"spender: {spender}")

    assert is_sorted, "Spenders address are not sorted in ascending order."
    print("All spenders' address are sorted in ascending order.")


@pytest.mark.parametrize("extract_values_from_response", [f"{BASE_URL_IDX}api/v1/events/GetByFiltersApprovals"],
                         indirect=True)
def test_spender_sort_desc(extract_values_from_response):
    url, _ = extract_values_from_response
    resp, body = fetch_get(url, params=['spenderSortDesc=true'])

    print(f"Status code: {resp.status_code}")
    assert resp.status_code == 200, f"Expected status code 200, but got {resp.status_code} instead."

    objs = body['values']
    # Create all spenders' list values
    values = [obj['spender'] for obj in objs]

    # Verify if the list is sorted
    is_sorted = all(values[i] >= values[i + 1] for i in range(len(values) - 1))

    for spender in values:
        print(f"spender: {spender}")

    assert is_sorted, "Spenders are not sorted in descending order."
    print("All spenders' address are sorted in descending order.")


@pytest.mark.parametrize("extract_values_from_response", [f"{BASE_URL_IDX}api/v1/events/GetByFiltersApprovals"],
                         indirect=True)
def test_tx_hash_filter(extract_values_from_response):
    url, random_values = extract_values_from_response
    txHash = random_values[5]
    resp, body = fetch_get(url, params=[f'txHash={txHash}'])

    print(f"Status code: {resp.status_code}")
    assert resp.status_code == 200, f"Expected status code 200, but got {resp.status_code} instead."

    objs = body['values']
    for obj in objs:
        print(f"txHash: {obj['txHash']}")
        assert_that(obj['txHash']).is_equal_to(txHash).described_as(
            f"The txHash filter is not working correctly."
            f"Expected txHash: '{txHash}' in the params, but got txHash: '{obj['txHash']}'"
            f" in the response objects.")
        assert_that(len(objs)).is_equal_to(int(body['total'])).described_as(
            f"Expected 'total' in response body ({body['total']}) to match the length of 'objs' ({len(objs)})")


@pytest.mark.parametrize("extract_values_from_response", [f"{BASE_URL_IDX}api/v1/events/GetByFiltersApprovals"],
                         indirect=True)
def test_log_index_filter(extract_values_from_response):
    url, random_values = extract_values_from_response
    logIndex = random_values[7]
    resp, body = fetch_get(url, params=[f'logIndex={logIndex}&limit={10000}'])

    print(f"Status code: {resp.status_code}")
    assert resp.status_code == 200, f"Expected status code 200, but got {resp.status_code} instead."

    objs = body['values']
    for obj in objs:
        print(f"logIndex: {obj['logIndex']}")
        assert_that(int(obj['logIndex'])).is_equal_to(logIndex).described_as(
            f"The logIndex filter is not working correctly."
            f"Expected logIndex: '{logIndex}' in the params, but got logIndex: '{obj['logIndex']}'"
            f" in the response objects.")
        assert_that(len(objs)).is_equal_to(int(body['total'])).described_as(
            f"Expected 'total' in response body ({body['total']}) to match the length of 'objs' ({len(objs)})")
    print(f"Total: {body['total']}")


@pytest.mark.parametrize("extract_values_from_response", [f"{BASE_URL_IDX}api/v1/events/GetByFiltersApprovals"],
                         indirect=True)
def test_indexed_at_filter(extract_values_from_response):
    url, random_values = extract_values_from_response
    indexedAt = random_values[6]
    resp, body = fetch_get(url, params=[f'indexedAt={indexedAt}'])

    print(f"Status code: {resp.status_code}")
    assert resp.status_code == 200, f"Expected status code 200, but got {resp.status_code} instead."

    objs = body['values']
    for obj in objs:
        print(f"indexedAt: {obj['indexedAt']}")
        assert_that(obj['indexedAt']).is_equal_to(indexedAt).described_as(
            f"The indexedAt filter is not working correctly."
            f"Expected indexedAt: '{indexedAt}' in the params, but got indexedAt: '{obj['indexedAt']}'"
            f" in the response objects.")
        assert_that(len(objs)).is_equal_to(int(body['total'])).described_as(
            f"Expected 'total' in response body ({body['total']}) to match the length of 'objs' ({len(objs)})")


@pytest.mark.parametrize("extract_values_from_response", [f"{BASE_URL_IDX}api/v1/events/GetByFiltersApprovals"],
                         indirect=True)
def test_random_limit(extract_values_from_response):
    url, _ = extract_values_from_response

    # Generate a random limit value
    random_limit = get_random_limit()

    resp, body = fetch_get(url, params=[f'limit={random_limit}'])

    print(f"Status code: {resp.status_code}")
    assert resp.status_code == 200, f"Expected status code 200, but got {resp.status_code} instead."

    objs = body['values']

    print(f"URL: {url}, Limit: {random_limit}, Object Count: {len(objs)}")

    assert_that(len(objs)).is_equal_to(random_limit).described_as(
        f"The number of objects returned in the response "
        f"{len(objs)} does not match the expected value {random_limit}")
