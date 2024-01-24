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
  clock: boolean = false
  time: string = ""

  dl_value: string = ""
  dpir1_value: number = 0
  dpir2_value: number = 0
  dus1_value: number = 0
  dus2_value: number = 0
  ds1_value: number = 0
  ds2_value: number = 0
  db_value: number = 0
  bb_value: number = 0
  rpir1_value: number = 0
  rpir2_value: number = 0
  rpir3_value: number = 0
  rpir4_value: number = 0
  gdht_temp_value: number = 0
  gdht_hum_value: number = 0
  b4sd_value: string = ""
  b4sd_placeholder: string = ""
  gsg_value: string = ""
  r: string = "0"
  g: string = "0"
  b: string = "0"
  redChecked: boolean = false
  greenChecked: boolean = false
  blueChecked: boolean = false

  rdht1_temp_value: number = 0
  rdht1_hum_value: number = 0
  rdht2_temp_value: number = 0
  rdht2_hum_value: number = 0
  rdht3_temp_value: number = 0
  rdht3_hum_value: number = 0
  rdht4_temp_value: number = 0
  rdht4_hum_value: number = 0

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
    this.socketService.get_clock().subscribe(message => {
      console.log(message)
      this.clock = true
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

    this.socketService.get_DPIR2().subscribe(message => {
      console.log(message)
      this.dpir2_value = message["value"]
    })

    this.socketService.get_DUS2().subscribe(message => {
      console.log(message)
      this.dus2_value = message["value"]
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

    this.socketService.get_BB().subscribe(message => {
      console.log(message)
      this.bb_value = message["value"]
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

    this.socketService.get_B4SD().subscribe(message => {
      console.log(message)
      this.b4sd_value = message["value"]
      this.b4sd_placeholder = message["value"]
    })
    setInterval(() => {
      this.blink_b4sd();
    }, 500);

    this.socketService.get_GSG().subscribe(message => {
      console.log(message)
      this.gsg_value = message["value"]
    })

    this.socketService.get_BIR().subscribe(message => {
      console.log(message)
      let bir: string = message["value"]
      let tokens: string[] = bir.split(":")
      this.r = tokens[0]
      this.g = tokens[1]
      this.b = tokens[2]
    })

    this.socketService.get_RDHT1_temp().subscribe(message => {
      console.log(message)
      this.rdht1_temp_value = message["value"]
    })

    this.socketService.get_RDHT1_hum().subscribe(message => {
      console.log(message)
      this.rdht1_hum_value = message["value"]
    })

    this.socketService.get_RDHT2_temp().subscribe(message => {
      console.log(message)
      this.rdht2_temp_value = message["value"]
    })

    this.socketService.get_RDHT2_hum().subscribe(message => {
      console.log(message)
      this.rdht2_hum_value = message["value"]
    })
    
    this.socketService.get_RDHT3_temp().subscribe(message => {
      console.log(message)
      this.rdht3_temp_value = message["value"]
    })

    this.socketService.get_RDHT3_hum().subscribe(message => {
      console.log(message)
      this.rdht3_hum_value = message["value"]
    })

    this.socketService.get_RDHT4_temp().subscribe(message => {
      console.log(message)
      this.rdht4_temp_value = message["value"]
    })

    this.socketService.get_RDHT4_hum().subscribe(message => {
      console.log(message)
      this.rdht4_hum_value = message["value"]
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

  send_clock() {
    this.socketService.send_clock(this.time).subscribe(data => {
      console.log("poslat time")
    })
  }

  stop_clock() {
    this.socketService.stop_clock().subscribe(data => {
      this.clock = false
    })
  }

  send_rgb() {
    let redValue = this.redChecked ? '1' : '0'
    let greenValue = this.greenChecked ? '1' : '0'
    let blueValue = this.blueChecked ? '1' : '0'

    let rgb = `${redValue}:${greenValue}:${blueValue}`

    this.socketService.send_rgb(rgb).subscribe(data => {
      console.log("poslat rgb")
    })
  }

  probaNaServer() {
    // this.socket.emit("probaNaServer", {"naserver": 123})
    this.clock = !this.clock
  }

  blink_b4sd() {
    if (this.clock)
      this.b4sd_value = this.b4sd_value === '' ? this.b4sd_placeholder : ''
    else
      this.b4sd_value = this.b4sd_placeholder
  }

}
