import json


def query(url, params):
    from gql import gql, Client
    from gql.transport.aiohttp import AIOHTTPTransport

    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url=url)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Provide a GraphQL query
    query = gql(
        """
        query GenerativeTokens($userId: String) {
            user(id: $userId) {
                name
                generativeTokens {
                    slug
                    entireCollection {
                        owner {
                            id
                        }
                        minter {
                            id
                            name
                        }
                    }
                }
            }
        }
        """
    )

    # Execute the query on the transport
    result = client.execute(query, variable_values=params)
    return result


if __name__ == '__main__':
    url = "https://api.fxhash.xyz/graphql/"
    params = {"userId": "tz1QYhY8YB8q1dxuFu4C7iA8odB5RaVgNLhX"}
    result = query(url, params)
    print(result)

    if result:
        with open("results.json", "w") as f:
            json.dump(result, f, indent=4)

