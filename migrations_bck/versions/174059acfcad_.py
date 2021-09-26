"""empty message

Revision ID: 174059acfcad
Revises: 
Create Date: 2021-09-23 00:13:26.149557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '174059acfcad'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('txns',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount_x', sa.String(), nullable=True),
    sa.Column('bidSignature', sa.String(), nullable=True),
    sa.Column('callDataHash', sa.String(), nullable=True),
    sa.Column('callTo', sa.String(), nullable=True),
    sa.Column('cancelCaller_x', sa.String(), nullable=True),
    sa.Column('cancelTransactionHash_x', sa.String(), nullable=True),
    sa.Column('chainId_x', sa.String(), nullable=True),
    sa.Column('expiry_x', sa.String(), nullable=True),
    sa.Column('fulfillCaller_x', sa.String(), nullable=True),
    sa.Column('fulfillTimestamp_x', sa.String(), nullable=True),
    sa.Column('fulfillTransactionHash_x', sa.String(), nullable=True),
    sa.Column('subgraphId', sa.String(), nullable=True),
    sa.Column('prepareCaller_x', sa.String(), nullable=True),
    sa.Column('prepareTransactionHash_x', sa.String(), nullable=True),
    sa.Column('preparedBlockNumber_x', sa.String(), nullable=True),
    sa.Column('preparedTimestamp_x', sa.String(), nullable=True),
    sa.Column('receivingAddress', sa.String(), nullable=True),
    sa.Column('receivingAssetId', sa.String(), nullable=True),
    sa.Column('receivingChainId', sa.String(), nullable=True),
    sa.Column('receivingChainTxManagerAddress', sa.String(), nullable=True),
    sa.Column('router', sa.String(), nullable=True),
    sa.Column('sendingAssetId', sa.String(), nullable=True),
    sa.Column('sendingChainFallback', sa.String(), nullable=True),
    sa.Column('sendingChainId', sa.String(), nullable=True),
    sa.Column('status_x', sa.String(), nullable=True),
    sa.Column('transactionId', sa.String(), nullable=True),
    sa.Column('user', sa.String(), nullable=True),
    sa.Column('chain_x', sa.String(), nullable=True),
    sa.Column('txn_type_x', sa.String(), nullable=True),
    sa.Column('asset_movement', sa.String(), nullable=True),
    sa.Column('asset_token', sa.String(), nullable=True),
    sa.Column('decimals_x', sa.Integer(), nullable=True),
    sa.Column('dollar_amount_x', sa.Float(), nullable=True),
    sa.Column('time_prepared_x', sa.DateTime(), nullable=True),
    sa.Column('time_fulfilled_x', sa.DateTime(), nullable=True),
    sa.Column('amount_y', sa.String(), nullable=True),
    sa.Column('cancelCaller_y', sa.String(), nullable=True),
    sa.Column('cancelTransactionHash_y', sa.String(), nullable=True),
    sa.Column('chainId_y', sa.String(), nullable=True),
    sa.Column('expiry_y', sa.String(), nullable=True),
    sa.Column('fulfillCaller_y', sa.String(), nullable=True),
    sa.Column('fulfillTimestamp_y', sa.String(), nullable=True),
    sa.Column('fulfillTransactionHash_y', sa.String(), nullable=True),
    sa.Column('prepareCaller_y', sa.String(), nullable=True),
    sa.Column('prepareTransactionHash_y', sa.String(), nullable=True),
    sa.Column('preparedBlockNumber_y', sa.String(), nullable=True),
    sa.Column('preparedTimestamp_y', sa.String(), nullable=True),
    sa.Column('status_y', sa.String(), nullable=True),
    sa.Column('chain_y', sa.String(), nullable=True),
    sa.Column('txn_type_y', sa.String(), nullable=True),
    sa.Column('decimals_y', sa.Integer(), nullable=True),
    sa.Column('dollar_amount_y', sa.Float(), nullable=True),
    sa.Column('time_prepared_y', sa.DateTime(), nullable=True),
    sa.Column('time_fulfilled_y', sa.DateTime(), nullable=True),
    sa.Column('time_taken', sa.Interval(), nullable=True),
    sa.Column('time_taken_seconds', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('txns')
    # ### end Alembic commands ###