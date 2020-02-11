schema = {
  "type": "object",
  "properties": {
    "parameters": {
      "type": "object",
      "properties": {
        "date": {
          "type": "string"
        },
        "location": {
          "type": "string"
        },
        "num_trustees": {
          "type": "string"
        },
        "threshold": {
          "type": "string"
        },
        "prime": {
          "type": "string"
        },
        "generator": {
          "type": "string"
        }
      },
      "required": [
        "date",
        "location",
        "num_trustees",
        "threshold",
        "prime",
        "generator"
      ]
    },
    "base_hash": {
      "type": "string"
    },
    "trustee_public_keys": {
      "type": "array",
      "items": {
          "type": "array",
          "items": {
              "type": "object",
              "properties": {
                "public_key": {
                  "type": "string"
                },
                "proof": {
                  "type": "object",
                  "properties": {
                    "commitment": {
                      "type": "string"
                    },
                    "challenge": {
                      "type": "string"
                    },
                    "response": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "commitment",
                    "challenge",
                    "response"
                  ]
                }
              },
              "required": [
                "public_key",
                "proof"
              ]
            }
        }
    },
    "joint_public_key": {
      "type": "string"
    },
    "extended_base_hash": {
      "type": "string"
    },
    "cast_ballots": {
      "type": "array",
      "items": {
          "type": "object",
          "properties": {
            "ballot_info": {
              "type": "object",
              "properties": {
                "date": {
                  "type": "string"
                },
                "device_info": {
                  "type": "string"
                },
                "time": {
                  "type": "string"
                },
                "tracker": {
                  "type": "string"
                }
              },
              "required": [
                "date",
                "device_info",
                "time",
                "tracker"
              ]
            },
            "contests": {
              "type": "array",
              "items": {
                  "type": "object",
                  "properties": {
                    "selections": {
                      "type": "array",
                      "items": {
                          "type": "object",
                          "properties": {
                            "message": {
                              "type": "object",
                              "properties": {
                                "public_key": {
                                  "type": "string"
                                },
                                "ciphertext": {
                                  "type": "string"
                                }
                              },
                              "required": [
                                "public_key",
                                "ciphertext"
                              ]
                            },
                            "zero_proof": {
                              "type": "object",
                              "properties": {
                                "commitment": {
                                  "type": "object",
                                  "properties": {
                                    "public_key": {
                                      "type": "string"
                                    },
                                    "ciphertext": {
                                      "type": "string"
                                    }
                                  },
                                  "required": [
                                    "public_key",
                                    "ciphertext"
                                  ]
                                },
                                "challenge": {
                                  "type": "string"
                                },
                                "response": {
                                  "type": "string"
                                }
                              },
                              "required": [
                                "commitment",
                                "challenge",
                                "response"
                              ]
                            },
                            "one_proof": {
                              "type": "object",
                              "properties": {
                                "commitment": {
                                  "type": "object",
                                  "properties": {
                                    "public_key": {
                                      "type": "string"
                                    },
                                    "ciphertext": {
                                      "type": "string"
                                    }
                                  },
                                  "required": [
                                    "public_key",
                                    "ciphertext"
                                  ]
                                },
                                "challenge": {
                                  "type": "string"
                                },
                                "response": {
                                  "type": "string"
                                }
                              },
                              "required": [
                                "commitment",
                                "challenge",
                                "response"
                              ]
                            }
                          },
                          "required": [
                            "message",
                            "zero_proof",
                            "one_proof"
                          ]
                        }
                    },
                    "max_selections": {
                      "type": "string"
                    },
                    "num_selections_proof": {
                      "type": "object",
                      "properties": {
                        "commitment": {
                          "type": "object",
                          "properties": {
                            "public_key": {
                              "type": "string"
                            },
                            "ciphertext": {
                              "type": "string"
                            }
                          },
                          "required": [
                            "public_key",
                            "ciphertext"
                          ]
                        },
                        "challenge": {
                          "type": "string"
                        },
                        "response": {
                          "type": "string"
                        }
                      },
                      "required": [
                        "commitment",
                        "challenge",
                        "response"
                      ]
                    }
                  },
                  "required": [
                    "selections",
                    "max_selections",
                    "num_selections_proof"
                  ]
                }
            }
          },
          "required": [
            "ballot_info",
            "contests"
          ]
        }
    },
    "contest_tallies": {
      "type": "array",
      "items": {
          "type": "array",
          "items": {
              "type": "object",
              "properties": {
                "cleartext": {
                  "type": "string"
                },
                "decrypted_tally": {
                  "type": "string"
                },
                "encrypted_tally": {
                  "type": "object",
                  "properties": {
                    "public_key": {
                      "type": "string"
                    },
                    "ciphertext": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "public_key",
                    "ciphertext"
                  ]
                },
                "shares": {
                  "type": "array",
                  "items": {
                      "type": "object",
                      "properties": {
                        "recovery": {
                          "type": "null"
                        },
                        "proof": {
                          "type": "object",
                          "properties": {
                            "commitment": {
                              "type": "object",
                              "properties": {
                                "public_key": {
                                  "type": "string"
                                },
                                "ciphertext": {
                                  "type": "string"
                                }
                              },
                              "required": [
                                "public_key",
                                "ciphertext"
                              ]
                            },
                            "challenge": {
                              "type": "string"
                            },
                            "response": {
                              "type": "string"
                            }
                          },
                          "required": [
                            "commitment",
                            "challenge",
                            "response"
                          ]
                        },
                        "share": {
                          "type": "string"
                        }
                      },
                      "required": [
                        "recovery",
                        "proof",
                        "share"
                      ]
                    }
                }
              },
              "required": [
                "cleartext",
                "decrypted_tally",
                "encrypted_tally",
                "shares"
              ]
            }
        }
    },
    "spoiled_ballots": {
      "type": "array",
      "items": {
          "type": "object",
          "properties": {
            "ballot_info": {
              "type": "object",
              "properties": {
                "date": {
                  "type": "string"
                },
                "device_info": {
                  "type": "string"
                },
                "time": {
                  "type": "string"
                },
                "tracker": {
                  "type": "string"
                }
              },
              "required": [
                "date",
                "device_info",
                "time",
                "tracker"
              ]
            },
            "contests": {
              "type": "array",
              "items": {
                  "type": "array",
                  "items": {
                      "type": "object",
                      "properties": {
                        "cleartext": {
                          "type": "string"
                        },
                        "decrypted_message": {
                          "type": "string"
                        },
                        "encrypted_message": {
                          "type": "object",
                          "properties": {
                            "public_key": {
                              "type": "string"
                            },
                            "ciphertext": {
                              "type": "string"
                            }
                          },
                          "required": [
                            "public_key",
                            "ciphertext"
                          ]
                        },
                        "shares": {
                          "type": "array",
                          "items": {
                              "type": "object",
                              "properties": {
                                "recovery": {
                                  "type": "null"
                                },
                                "proof": {
                                  "type": "object",
                                  "properties": {
                                    "commitment": {
                                      "type": "object",
                                      "properties": {
                                        "public_key": {
                                          "type": "string"
                                        },
                                        "ciphertext": {
                                          "type": "string"
                                        }
                                      },
                                      "required": [
                                        "public_key",
                                        "ciphertext"
                                      ]
                                    },
                                    "challenge": {
                                      "type": "string"
                                    },
                                    "response": {
                                      "type": "string"
                                    }
                                  },
                                  "required": [
                                    "commitment",
                                    "challenge",
                                    "response"
                                  ]
                                },
                                "share": {
                                  "type": "string"
                                }
                              },
                              "required": [
                                "recovery",
                                "proof",
                                "share"
                              ]
                            },
                        }
                      },
                      "required": [
                        "cleartext",
                        "decrypted_message",
                        "encrypted_message",
                        "shares"
                      ]
                    }
                }
            }
          },
          "required": [
            "ballot_info",
            "contests"
          ]
        }
    }
  },
  "required": [
    "parameters",
    "base_hash",
    "trustee_public_keys",
    "joint_public_key",
    "extended_base_hash",
    "cast_ballots",
    "contest_tallies",
    "spoiled_ballots"
  ]
}
