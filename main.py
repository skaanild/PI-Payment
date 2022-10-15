from stellar_sdk import Asset, Keypair, Network, Server, TransactionBuilder
from stellar_sdk.exceptions import NotFoundError, BadResponseError, BadRequestError


phrases = '' # Put you wallet secret phrase here
pair = Keypair.from_mnemonic_phrase(phrases) # get wallet secret Key


server = Server("https://horizon-testnet.stellar.org")
source_key = Keypair.from_mnemonic_phrase(phrases)
destination_id = "" # Receiver wallet ID

try:
    server.load_account(destination_id)
except NotFoundError:
    # If the account is not found, surface an error message for logging.
    raise Exception("The destination account does not exist!")


source_account = server.load_account(source_key.public_key)
base_fee = server.fetch_base_fee()


transaction = (
    TransactionBuilder(
        source_account=source_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=base_fee,
    )
        # Because Stellar allows transaction in many currencies, you must specify the asset type.
        # Here we are sending Lumens.
        .append_payment_op(destination=destination_id, asset=Asset.native(), amount="0.11")
        # A memo allows you to add your own metadata to a transaction. It's
        # optional and does not affect how Stellar treats the transaction.
        .add_text_memo("Test Transaction")
        # Wait a maximum of three minutes for the transaction
        .set_timeout(30)
        .build()
)


try:
    # And finally, send it off to Stellar!
    response = server.submit_transaction(transaction)
    print(f"Response: {response}")
except (BadRequestError, BadResponseError) as err:
    print(f"Something went wrong!\n{err}")