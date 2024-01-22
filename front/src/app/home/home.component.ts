import { Component, OnInit } from '@angular/core';
import { SocketService } from './socket.service';
import { Socket } from 'ngx-socket-io';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  constructor(private socketService: SocketService, private socket: Socket) { }

  persons: number = 0
  alarm: boolean = false
  active: boolean = false
  pin: string = ""

  dl_value: string = ""
  dpir1_value: number = 0
  dus1_value: number = 0
  ds1_value: number = 0
  ds2_value: number = 0
  db_value: number = 0
  rpir1_value: number = 0
  rpir2_value: number = 0
  rpir3_value: number = 0
  rpir4_value: number = 0
  gdht_temp_value: number = 0
  gdht_hum_value: number = 0

  ngOnInit(): void {
    this.socketService.getMessage().subscribe(message => {
      console.log(message)
    })

    this.socketService.get_persons().subscribe(message => {
      console.log(message)
      this.persons = message["value"]
    })
    this.socketService.get_alarm().subscribe(message => {
      console.log(message)
      this.alarm = message["value"]
    })
    this.socketService.get_active().subscribe(message => {
      console.log(message)
      this.active = message["value"]
    })

    this.socketService.get_DL().subscribe(message => {
      console.log(message)
      this.dl_value = message["value"]
    })

    this.socketService.get_DPIR1().subscribe(message => {
      console.log(message)
      this.dpir1_value = message["value"]
    })

    this.socketService.get_DUS1().subscribe(message => {
      console.log(message)
      this.dus1_value = message["value"]
    })

    this.socketService.get_DS1().subscribe(message => {
      console.log(message)
      this.ds1_value = message["value"]
    })

    this.socketService.get_DS2().subscribe(message => {
      console.log(message)
      this.ds2_value = message["value"]
    })

    this.socketService.get_DB().subscribe(message => {
      console.log(message)
      this.db_value = message["value"]
    })

    this.socketService.get_RPIR1().subscribe(message => {
      console.log(message)
      this.rpir1_value = message["value"]
    })

    this.socketService.get_RPIR2().subscribe(message => {
      console.log(message)
      this.rpir2_value = message["value"]
    })

    this.socketService.get_RPIR3().subscribe(message => {
      console.log(message)
      this.rpir3_value = message["value"]
    })

    this.socketService.get_RPIR4().subscribe(message => {
      console.log(message)
      this.rpir4_value = message["value"]
    })

    this.socketService.get_GDHT_temp().subscribe(message => {
      console.log(message)
      this.gdht_temp_value = message["value"]
    })

    this.socketService.get_GDHT_hum().subscribe(message => {
      console.log(message)
      this.gdht_hum_value = message["value"]
    })
  }

  send_alarm_pin() {
    this.socketService.send_pin(this.pin).subscribe(data => {
      console.log("poslat pin")
    })
  }

  send_activate_pin() {
    this.socketService.send_activate_pin(this.pin).subscribe(data => {
      console.log("poslat activate pin")
    })
  }

  probaNaServer() {
    this.socket.emit("probaNaServer", {"naserver": 123})
  }

}
