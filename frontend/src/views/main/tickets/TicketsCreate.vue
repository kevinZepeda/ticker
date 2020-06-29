categories1<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Create Ticket</div>
      </v-card-title>
      <v-card-text>
        <template>
          <v-form v-model="valid" ref="form" lazy-validation>
            <v-text-field label="Title" v-model="title" required></v-text-field>
            <v-text-field label="Description" v-model="description" required></v-text-field>
            <table>
              <tr>
                <th><v-select v-model="ticketType" :items="this.typesOfTickets" label="Ticket Type" outlined></v-select></th>
                <th><v-text-field label="external Id" v-model="externalId" required></v-text-field></th>
                <th><v-select v-model="tenant" :items="this.tenants" label="Tenant" outlined></v-select></th>
              </tr>
              <tr>
                <th><v-select v-model="region" :items="this.regions" label="Region" outlined></v-select></th>
                <th><v-select v-model="requestType" :items="this.requests" label="Request Type" outlined></v-select></th>
                <th><v-select v-model="vlan" :items="this.vlans" label="VLAN" outlined></v-select></th>
                <th><v-select v-model="vrf" :items="this.vrfs" label="VRF" outlined></v-select></th>
              </tr>
              <tr>
                <th><v-select v-model="category1" :items="this.categories1" label="Category 1" outlined></v-select></th>
                <th><v-select v-model="category2" :items="this.categories2" label="Category 2" outlined></v-select></th>
                <th><v-select v-model="category3" :items="this.categories3" label="Category 3" outlined></v-select></th>
              </tr>
            </table>
            <v-textarea
              outlined
              v-model="devices"
              label="IP's separated by enter"
              required
            ></v-textarea>
            <div class="subheading secondary--text text--lighten-2">Ticket is active <span v-if="isActive">(currently active)</span><span v-else>(currently not active)</span></div>
            <v-checkbox label="Is Active" v-model="isActive"></v-checkbox>
          </v-form>
        </template>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="cancel">Cancel</v-btn>
        <v-btn @click="reset">Reset</v-btn>
        <v-btn @click="submit" :disabled="!valid">
              Save
            </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import axios from 'axios';
import {
  IUserTicket,
  IUserTicketUpdate,
  IUserTicketCreate,
  IDevices,
} from '@/interfaces';
import { dispatchGetTickets, dispatchCreateTicket } from '@/store/admin/actions';

// import { dispatchGetDevices } from '@/store/admin/actions';

@Component
export default class CreateTicket extends Vue {
  public valid = false;
  public title: string = '';
  public description: string = '';
  public devices: string = '';
  public ticketType: string = '';
  public externalId: number = 0;
  public tenant: string = '';
  public region: string = '';
  public requestType: string = '';
  public category1: string = '';
  public category2: string = '';
  public category3: string = '';
  public vlan: string = '';
  public vrf: string = '';
  public isActive: number = 1;
  public typesOfTickets;
  public vrfs;
  public tenants;
  public vlans;
  public regions;
  public requests;
  public categories1;
  public categories2;
  public categories3;



  public async mounted() {
    await dispatchGetTickets(this.$store);
    this.reset();
    axios.get('http://netbox.kinetworking.com:32768/api/ipam/vrfs/' , {
      headers: {
        Authorization: 'Token 0123456789abcdef0123456789abcdef01234567',
      },
      params: {
        format: 'json',
      },
    }).then( (response) => {
      const dataObj = response.data.results;
      this.vrfs = dataObj.map( (value) => {
        return { text: value.name , value: value.id };
      });
    });

    axios.get('http://netbox.kinetworking.com:32768/api/tenancy/tenants/' , {
      headers: {
        Authorization: 'Token 0123456789abcdef0123456789abcdef01234567',
      },
      params: {
        format: 'json',
      },
    }).then( (response) => {
      const dataObj = response.data.results;
      this.tenants = dataObj.map( (value) => {
        return { text: value.name , value: value.id };
      });
    });

    axios.get('http://netbox.kinetworking.com:32768/api/ipam/vlans/' , {
      headers: {
        Authorization: 'Token 0123456789abcdef0123456789abcdef01234567',
      },
      params: {
        format: 'json',
      },
    }).then( (response) => {
      const dataObj = response.data.results;
      this.vlans = dataObj.map( (value) => {
        return { text: value.id , value: value.id };
      });
    });
  }

  public reset() {
    this.title = '';
    this.description = '';
    this.devices = '';
    this.isActive = 0;
    this.ticketType = '';
    this.externalId = 0;
    this.tenant = '';
    this.region = '';
    this.requestType = '';
    this.category1 = '';
    this.category2 = '';
    this.category3 = '';
    this.vlan = '';
    this.vrf = '';
    this.typesOfTickets = ['Allocate', 'Relase'];
    this.requests = ['IP'];
    this.regions = ['Region 1', 'Region 2', 'Region 3', 'Region 4', 'Region 5', 'Region 6', 'Region 7', 'Region 8', 'Region 9'];
    this.$validator.reset();
    this.categories1 = ['Routable', 'Non-Routeable'];
    this.categories2 = ['Public', 'Private'];
    this.categories3 = ['Active', 'Reserved'];
   }

  public cancel() {
    this.$router.back();
  }
  public async submit() {
    const listIps = this.devices.split('\n');

    if (this.isActive) {
      for (const i of listIps) {
        axios.post('http://netbox.kinetworking.com:32768/api/ipam/ip-addresses/' , {
          address: i,
          status: 'active',
          description: this.description,
          tenant: this.tenant,
          vrf: this.vrf,
          tags: [
            this.category1,
            this.category2,
            this.category3,
          ],
        }, {
          headers: {
            'Authorization': 'Token 0123456789abcdef0123456789abcdef01234567',
            'Content-Type': 'application/json',
            'Accept': 'application/json; indent=4',
          },
        }).then( (response) => {
          console.log(response)
        });
      }
    }

    if (await this.$validator.validateAll()) {
      const updatedTicket: IUserTicketCreate = {
        devices: this.devices,
      };
      if (this.title) {
        updatedTicket.title = this.title;
      }
      if (this.description) {
        updatedTicket.description = this.description;
      }
      if (this.devices) {
        updatedTicket.devices = this.devices;
      }
      if (this.ticketType) {
        updatedTicket.ticketType = this.ticketType;
      }
      if (this.externalId) {
        updatedTicket.externalId = this.externalId;
      }
      if (this.tenant) {
        updatedTicket.tenant = this.tenant;
      }
      if (this.region) {
        updatedTicket.region = this.region;
      }
      if (this.requestType) {
        updatedTicket.requestType = this.requestType;
      }
      if (this.category1) {
        updatedTicket.category1 = this.category1;
      }
      if (this.category2) {
        updatedTicket.category2 = this.category2;
      }
      if (this.category3) {
        updatedTicket.category3 = this.category3;
      }
      if (this.vlan) {
        updatedTicket.vlan = this.vlan;
      }
      if (this.vrf) {
        updatedTicket.vrf = this.vrf;
      }
      updatedTicket.is_active = this.isActive;
      await dispatchCreateTicket(this.$store, updatedTicket);
      this.$router.push('/main/tickets');
    }
  }
}

</script>
