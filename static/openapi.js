var spec = {
  "openapi": "3.0.1",
  "info": {
    "version": "1.0.0",
    "title": "Elevators API"
  },
  "paths": {
    "/elevators": {
      "post": {
        "summary": "Call elevator according to filter",
        "operationId": "findElevator",
        "tags": [
          "Elevator API"
        ],
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/Request"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Success",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ElevatorsList"
                }
              }
            }
          },
          "400": {
            "$ref": "#/components/responses/IllegalInput"
          }
        }
      },
      "get": {
        "summary": "Get a list of elevators",
        "operationId": "listElevators",
        "tags": [
          "Elevator API"
        ],
        "responses": {
          "200": {
            "description": "Success",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ElevatorsList"
                }
              }
            }
          }
        }
      }
    },
    "/elevators/{name}": {
      "get": {
        "summary": "Get an elevator ",
        "operationId": "getElevator",
        "tags": [
          "Elevator API"
        ],
        "parameters": [
          {
             "in": "path",
             "name": "name",
             "required": true,
             "description" : "Elevator name",
             "schema" : {"type" : "string"}
          }
        ],
        "responses": {
          "200": {
            "description": "Success",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Elevator"
                }
              }
            }
          },
          "404": {
            "$ref": "#/components/responses/NotFound"
          }
        }
      },
    },
  },
  "components": {
    "schemas": {
      "Request" : {
        "description" : "Elevator Request",
        "required": ["num_persons","cargo_weight","floor"],
        "properties": {
          "num_persons": {
            "description": "Number of persons",
            "type": "integer",
            "example": "4"
          },
          "cargo_weight": {
            "description": "Cargo weight",
            "type": "integer",
            "example": "100"
          },
          "floor": {
            "description": "Wanted floor",
            "type": "integer",
            "example": "8"
          }
        }
      },
      "ElevatorsList":{
        "description" : "Elevators list",
        "type": "array",
        "items": {
          "$ref": "#/components/schemas/Elevator"
        }         
      }
    }
  }

  /*
  "components": {
    "schemas": {
      "Id": {
        "description": "Resource ID",
        "type": "integer",
        "format": "int64",
        "readOnly": true,
        "example": 1
      },
      "ArticleForList": {
        "properties": {
          "id": {
            "$ref": "#/components/schemas/Id"
          },
          "category": {
            "description": "Category of an article",
            "type": "string",
            "example": "sports"
          }
        }
      },
      "Article": {
        "allOf": [
          {
            "$ref": "#/components/schemas/ArticleForList"
          }
        ],
        "required": [
          "text"
        ],
        "properties": {
          "text": {
            "description": "Content of an article",
            "type": "string",
            "maxLength": 1024,
            "example": "# Title\n\n## Head Line\n\nBody"
          }
        }
      },
      "ArticleList": {
        "type": "array",
        "items": {
          "$ref": "#/components/schemas/ArticleForList"
        }
      },
      "Error": {
        "description": "<table>\n  <tr>\n    <th>Code</th>\n    <th>Description</th>\n  </tr>\n  <tr>\n    <td>illegal_input</td>\n    <td>The input is invalid.</td>\n  </tr>\n  <tr>\n    <td>not_found</td>\n    <td>The resource is not found.</td>\n  </tr>\n</table>\n",
        "required": [
          "code",
          "message"
        ],
        "properties": {
          "code": {
            "type": "string",
            "example": "illegal_input"
          }
        }
      }
    },
    "parameters": {
      "Id": {
        "name": "id",
        "in": "path",
        "description": "Resource ID",
        "required": true,
        "schema": {
          "$ref": "#/components/schemas/Id"
        }
      },
      "Limit": {
        "name": "limit",
        "in": "query",
        "description": "limit",
        "required": false,
        "schema": {
          "type": "integer",
          "minimum": 1,
          "maximum": 100,
          "default": 10,
          "example": 10
        }
      },
      "Offset": {
        "name": "offset",
        "in": "query",
        "description": "offset",
        "required": false,
        "schema": {
          "type": "integer",
          "minimum": 0,
          "default": 0,
          "example": 10
        }
      }
    },
    "responses": {
      "NotFound": {
        "description": "The resource is not found.",
        "content": {
          "application/json": {
            "schema": {
              "$ref": "#/components/schemas/Error"
            }
          }
        }
      },
      "IllegalInput": {
        "description": "The input is invalid.",
        "content": {
          "application/json": {
            "schema": {
              "$ref": "#/components/schemas/Error"
            }
          }
        }
      }
    }
  }
  */
}
