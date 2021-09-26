from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from data.constants import (
    txn_columns,
    txns_params,
    txns_query,
    last_blocs,
    chain_asset_data,
    chain_mapping,
)
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

transport_matic = AIOHTTPTransport(
    url="https://api.thegraph.com/subgraphs/name/0xakshay/nxtpmatic"
)
transport_bsc = AIOHTTPTransport(
    url="https://api.thegraph.com/subgraphs/name/0xakshay/nxtpbsc"
)
transport_xdai = AIOHTTPTransport(
    url="https://api.thegraph.com/subgraphs/name/0xakshay/nxtpxdai"
)
transport_fantom = AIOHTTPTransport(
    url="https://api.thegraph.com/subgraphs/name/0xakshay/nxtpfantom"
)
transport_arbitrum = AIOHTTPTransport(
    url="https://api.thegraph.com/subgraphs/name/0xakshay/nxtparbitrum"
)


def concat_dfs(main_df, new_df):
    new_df.drop_duplicates(inplace=True)
    result = pd.concat([main_df, new_df])
    result.drop_duplicates(inplace=True)
    result.reset_index(inplace=True, drop=True)
    return result


def fetch_chain_transactions(query, params, transport, chain, expiry_cut_off):

    dataframe = pd.DataFrame(columns=txn_columns)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    params["expiryTime"] = expiry_cut_off
    while True:  # Just a random no.
        result = client.execute(query, params)

        for tr in result["transactions"]:
            list_values = list(tr.values())
            list_values[12] = list_values[12]["id"]
            dataframe.loc[len(dataframe.index)] = list_values
        if len(result["transactions"]) == 0:
            break
        params["expiryTime"] = result["transactions"][-1]["expiry"]
        if len(result["transactions"]) < 1000:
            break
    print(dataframe.shape[0], end="-")
    print("Fetched from", chain)
    return dataframe


def transacting_chains(row):
    val = (
        chain_mapping[row["sendingChainId"]]
        + " -> "
        + chain_mapping[row["receivingChainId"]]
    )
    return val


def asset_token_mapper(row):
    chain_asset_dict = chain_asset_data[row["chain"]]
    if row["txn_type"] == "repeat":
        asset = chain_asset_dict[row["receivingAssetId"]]
    else:
        asset = chain_asset_dict[row["sendingAssetId"]]
    return asset["token"]


def asset_decimal_mapper(row):
    chain_asset_dict = chain_asset_data[row["chain"]]
    if row["txn_type"] == "repeat":
        asset = chain_asset_dict[row["receivingAssetId"]]
    else:
        asset = chain_asset_dict[row["sendingAssetId"]]
    return asset["decimals"]


def dollar_amount(row):
    dollar_value = int(row["amount"]) / 10 ** row["decimals"]
    return dollar_value


def time_taken(row):
    time_taken = row["time_fulfilled_y"] - row["time_prepared_x"]
    return time_taken


def fetch_txns_df(expiry_cut_off):
    matic_txns = pd.DataFrame(columns=txn_columns)
    bsc_txns = pd.DataFrame(columns=txn_columns)
    xdai_txns = pd.DataFrame(columns=txn_columns)
    fantom_txns = pd.DataFrame(columns=txn_columns)
    arbitrum_txns = pd.DataFrame(columns=txn_columns)

    new_df = fetch_chain_transactions(
        txns_query, txns_params, transport_matic, "Polygon", expiry_cut_off
    )
    matic_txns = concat_dfs(matic_txns, new_df)

    new_df = fetch_chain_transactions(
        txns_query, txns_params, transport_bsc, "BSC", expiry_cut_off
    )
    bsc_txns = concat_dfs(bsc_txns, new_df)

    new_df = fetch_chain_transactions(
        txns_query, txns_params, transport_xdai, "xDai", expiry_cut_off
    )
    xdai_txns = concat_dfs(xdai_txns, new_df)

    new_df = fetch_chain_transactions(
        txns_query, txns_params, transport_fantom, "Fantom", expiry_cut_off
    )
    fantom_txns = concat_dfs(fantom_txns, new_df)

    new_df = fetch_chain_transactions(
        txns_query, txns_params, transport_arbitrum, "Arbitrum", expiry_cut_off
    )
    arbitrum_txns = concat_dfs(arbitrum_txns, new_df)

    matic_txns["chain"] = "Polygon"
    bsc_txns["chain"] = "BSC"
    xdai_txns["chain"] = "xDai"
    fantom_txns["chain"] = "Fantom"
    arbitrum_txns["chain"] = "Arbitrum"

    two_sided_txns = pd.concat(
        [matic_txns, bsc_txns, xdai_txns, fantom_txns, arbitrum_txns]
    )
    if two_sided_txns.shape[0] == 0:
        print("No new rows to add")
        return two_sided_txns
    two_sided_txns["txn_type"] = two_sided_txns.apply(
        lambda x: "single" if x["sendingChainId"] == x["chainId"] else "repeat", axis=1
    )

    two_sided_txns["asset_movement"] = two_sided_txns.apply(transacting_chains, axis=1)

    two_sided_txns["asset_token"] = two_sided_txns.apply(asset_token_mapper, axis=1)
    two_sided_txns["decimals"] = two_sided_txns.apply(asset_decimal_mapper, axis=1)

    two_sided_txns["dollar_amount"] = two_sided_txns.apply(dollar_amount, axis=1)

    two_sided_txns["time_prepared"] = two_sided_txns["preparedTimestamp"].apply(
        lambda x: pd.to_datetime(x, unit="s")
    )

    two_sided_txns["time_fulfilled"] = two_sided_txns["fulfillTimestamp"].apply(
        lambda x: pd.to_datetime(x, unit="s")
    )

    print(two_sided_txns.shape)
    compact_data_txns = two_sided_txns.drop(
        ["receivingChainId", "chainId", "sendingChainId"], axis=1
    )

    repeat_txns = compact_data_txns[compact_data_txns["txn_type"] == "repeat"].copy(
        deep=True
    )
    one_sided_txns = compact_data_txns[compact_data_txns["txn_type"] == "single"].copy(
        deep=True
    )
    repeat_txns.reset_index(drop=True, inplace=True)
    one_sided_txns.reset_index(drop=True, inplace=True)

    dem2_merge_cols = [
        "id",
        "receivingAssetId",
        "asset_token",
        "user",
        "sendingAssetId",
        "receivingChainId",
        "receivingAddress",
        "asset_movement",
        "sendingChainId",
    ]
    merged_txns = pd.merge(
        left=one_sided_txns,
        right=repeat_txns,
        how="outer",
        left_on=dem2_merge_cols,
        right_on=dem2_merge_cols,
    )
    print("Merged", merged_txns.shape)
    merged_txns["time_taken"] = merged_txns.apply(time_taken, axis=1)
    merged_txns["time_taken_seconds"] = merged_txns["time_taken"].apply(
        lambda x: x.seconds
    )

    merged_txns.replace({np.NaN: None}, inplace=True)
    # fulfilled_txns = merged_txns[
    #     (merged_txns.status_x == "Fulfilled") & (merged_txns.status_y == "Fulfilled")
    # ].copy(deep=True)

    return merged_txns