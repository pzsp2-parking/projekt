import { React } from 'react';
import { Chart } from 'react-charts'


function ChargeChart(props) {
    const chargeData = props.chargeData.map(el => {return {
      x: new Date(el.x),
      y: el.y
    }})
  
    const data = [
        {
          label: 'Series 1',
          data: chargeData
        }
      ]
   
    const axes = [
        { primary: true, type: 'utc', position: 'bottom' },
        { type: 'linear', hardMin: 0, hardMax:100, position: 'left' }
      ]
   
    return (
      <div
        style={{
          width: '400px',
          height: '300px'
        }}
      >
        <Chart data={data} axes={axes} />
      </div>
    )
  }

  export default ChargeChart;