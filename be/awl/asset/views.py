from django.shortcuts import render
from .models import Asset
from .serializer import AssetSerializer
# from rest_framework import viewsets
# from rest_framework.authentication import BasicAuthentication
# from rest_framework.permissions import IsAuthenicated
from rest_framework.response import Response
from rest_framework.decorators import api_view

import requests
from .coinlist import coins

cmc_key = 'API_KEY'

def fetch_asset_data(ID, SYMBOL):
    coin_id = str(coins[SYMBOL.upper()])
    if coin_id:
        url = f'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
        headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': cmc_key,
        }
        r = requests.get(url, headers=headers, params={'id':coin_id})
        data = r.json()

        quote = round(float(data['data'][coin_id]['quote']['USD']['price']),2) if data['data'][coin_id]['quote']['USD']['price'] > 1 else round(float(data['data'][coin_id]['quote']['USD']['price']),4)
        mrkt_cap = round(float(data['data'][coin_id]['quote']['USD']['market_cap']))
        vol = round(float(data['data'][coin_id]['quote']['USD']['volume_24h']))
        change_day = round(float(data['data'][coin_id]['quote']['USD']['percent_change_24h']),2)
        change_week = round(float(data['data'][coin_id]['quote']['USD']['percent_change_7d']),2)
        change_month = round(float(data['data'][coin_id]['quote']['USD']['percent_change_30d']),2)

        asset_obj = {
            "id" : ID,
            "coin_id" : coin_id,
            "symbol" : SYMBOL.upper(),
            "quote" : quote,
            "mrkt_cap" : mrkt_cap,
            "vol" : vol,
            "change_day" : change_day,
            "change_week" : change_week,
            "change_month" : change_month
        }

        return asset_obj
    else:
        return 'Error finding asset.'

## Describe what is available from API
@api_view(['GET'])
def apiOverview(req):
    api_urls = {
        'List' : '/asset-list/',
        'Detail' : '/asset-list/<str:pk>/',
        'Create' : '/asset-create/',
        'Update' : '/asset-update/<str:pk>/',
        'Delete' : '/asset-delete/<str:pk>/',
    }

    return Response(api_urls)

## Return all objects in DB
@api_view(['GET'])
def asset_list(req):
    assets = Asset.objects.all()
    # many = true when serializing all object, false when one object to serialize
    serializer_context = {'request': req}
    serializer = AssetSerializer(assets, context=serializer_context, many=True)
    return Response(serializer.data)

## Return detail of one object
@api_view(['GET'])
def asset_detail(req, pk):
    asset = Asset.objects.get(id=pk)
    serializer_context = {'request': req}
    serializer = AssetSerializer(asset, context=serializer_context, many=False)
    return Response(serializer.data)

## Create a new asset
@api_view(['POST'])
def asset_create(req):
    ## req.data sends us a json obj
    asset = req.data['symbol']
    data = fetch_asset_data(0, asset)
    serializer_context = {'request': req}
    serializer = AssetSerializer(context=serializer_context, data=data)
    
    ## check if json form matches schema, send item back to DB & save
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)

    return Response(serializer.data)

## Update an existing asset record - in this method we should call the yahoo finance app
@api_view(['GET'])
def asset_update(req, pk):
    asset = Asset.objects.get(id=pk)
    data = fetch_asset_data(asset.id, asset.symbol)
    ## Set the serializer to the instance of this record to update it with the data from form.
    serializer_context = {'request': req}
    serializer = AssetSerializer(instance=asset, context=serializer_context, data = data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

## Updates all quotes currently in watchlist.
@api_view(['GET'])
def asset_update_all(req):
    assets = Asset.objects.all()

    for asset in assets:
        data = fetch_asset_data(asset.id, asset.symbol)
        serializer_context = {'request': req}
        serializer = AssetSerializer(instance=asset, context=serializer_context, data = data)

        if serializer.is_valid():
            serializer.save()
    # many = true when serializing all object, false when one object to serialize

    assets = Asset.objects.all()
    serializer_context = {'request': req}
    serializer = AssetSerializer(assets, context=serializer_context, many=True)
    return Response(serializer.data)

## Delete an existing asset record
@api_view(['DELETE'])
def asset_delete(req, pk):
    asset = Asset.objects.get(id=pk)
    asset.delete()

    return Response(f'Item {pk} was deleted.')

