from ariadne import gql

type_defs = gql("""
    type Search {
        name: String!
        sex: String!
    }
    type Query {
        search(keyword: String!): Search
    }
""")
