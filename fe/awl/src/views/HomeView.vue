<template>
  <div class="home">
    <div class="container-width">
      <div class="ui secondary borderless menu">
        <a href="#" class="ui item">
          Home
        </a>
        <div class="right menu">
          <a class="ui item">
            Sign In
          </a>
        </div>
      </div>
      <h1 class="flex-title">Asset Watch List</h1>
      <div class="ui raised segment container">
        <div class="ui middle aligned stackable grid">
          <div class="five wide column">
            <form @submit.prevent="add_asset">
              <div class="ui action input focus field">
                  <input type="text" placeholder="Add Asset" name='symbol' v-model="symbol">
                  <button class="ui icon button green is-link" type="submit"><i class="add icon" ></i></button>
              </div>    
            </form>
          </div>
          <div class="seven wide column">
            <form @submit.prevent="get_assets" class="ui form">
              <div class="inline fields">
                <div class="field">
                  <div class="ui radio checkbox">
                    <input type="radio" name="filter" checked="checked" v-model="filter" v-bind:value="'all'">
                    <label>Show All</label>
                  </div>
                </div>
                <div class="field">
                  <div class="ui radio checkbox">
                    <input type="radio" name="filter" v-model="filter" v-bind:value="'pump'">
                    <label>Daily Pump</label>
                  </div>
                </div>
                <div class="field">
                  <div class="ui radio checkbox">
                    <input type="radio" name="filter" v-model="filter" v-bind:value="'dump'">
                    <label>Daily Dump</label>
                  </div>
                </div>
                <button class='ui inverted button' type="submit">
                  <div id="filter_assets" class="ui animated button blue">
                    <div class="visible content">Filter</div>
                      <div class="hidden content">
                        <i class="filter icon is-link"></i>
                      </div>
                  </div>
                </button>
              </div>
            </form>
          </div>
          <div class="four wide column">
            <div id="update_assets" class="ui animated button yellow" @click="update_assets()">
              <div class="visible content">Update Quotes</div>
                <div class="hidden content">
                  <i class="sync icon"></i>
                </div>
            </div>
          </div>
        </div>
      </div>
      <div class="ui container">
          <table class="ui celled striped blue inverted table">
            <thead>
              <tr class="center aligned">
                <th>Symbol</th>
                <th>Quote</th>
                <th>Market Cap</th>
                <th>24H Volume</th>
                <th>24H Change</th>
                <th>7D Change</th>
                <th>30D Change</th>
                <th>Remove</th>
              </tr>
            </thead>
            <tbody>
              <tr class="center aligned" v-for="asset in assets" :key="asset.id">
                <td class="selectable">
                  <a href="">{{ asset.symbol }}</a>
                </td>
                <td>$ {{ Intl.NumberFormat('en-US').format(asset.quote) }}</td>
                <td>{{ Intl.NumberFormat('en-US').format(asset.mrkt_cap) }}</td>
                <td>{{ Intl.NumberFormat('en-US').format(asset.vol) }}</td>
                <td>{{ asset.change_day }} %</td>
                <td>{{ asset.change_week }} %</td>
                <td>{{ asset.change_month }} %</td>
                <td><button class="ui icon button mini red" id="add_asset" @click="remove_asset(asset.id)"><i class="trash alternate icon" id="remove_asset" ></i></button></td>
              </tr>
            </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Modal from '../components/Modal.vue'

export default {
  name: 'HomeView',
  components: {
    Modal,
  },
  data() {
    return {
      assets : [],
      symbol : '',
      filter : 'all'
    }
  },
  mounted() {
    this.get_assets()
  },
  methods : {
    get_assets() {
      axios({
        method:'get',
        url:'http://127.0.0.1:8000/asset/asset-list/',
        auth: {
          username:'BASIC_USER',
          password:'BASIC_PWD'
        }
      }).then(resp=> {
        
        switch(this.filter) {
          case 'all':
            this.assets = resp.data
            break;
          case 'pump':
            this.assets = resp.data.filter((asset) => asset.change_day > 0.0)
            break;
          case 'dump':
            this.assets = resp.data.filter((asset) => asset.change_day < 0.0)
            break;     
      }
      })
    },
    add_asset() {
      if(this.symbol) {
        axios({
          method: 'post',
          url: 'http://127.0.0.1:8000/asset/asset-create/',
          data: {
            'symbol': this.symbol
          },
          auth: {
            username:'BASIC_USER',
            password:'BASIC_PWD'
          }
        }).then(resp => {
          let newAsset = {
            'id' : resp.data.id,
            'symbol' : resp.data.symbol,
            'quote' : resp.data.quote,
            'mrkt_cap' : resp.data.mrkt_cap,
            'vol' : resp.data.vol,
            'change_day' : resp.data.change_day,
            'change_week' : resp.data.change_week,
            'change_month' : resp.data.change_month
          }

          this.assets.push(newAsset)
          this.symbol = ''
        }).catch((err) => console.log(err))
      }

    },
    remove_asset(asset_id) {
      axios({
        method: 'delete',
        url: 'http://127.0.0.1:8000/asset/asset-delete/' + asset_id,
        auth: {
          username:'BASIC_USER',
          password:'BASIC_PWD'
        }
      }).then()

      this.assets = this.assets.filter((asset) => asset.id !== asset_id)
    },
    update_assets() {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/asset/asset-update-all/',
        auth: {
          username:'BASIC_USER',
          password:'BASIC_PWD'
        }
      }).then(resp=> this.assets = resp.data)
    },  
  }
}
</script>
