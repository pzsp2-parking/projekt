import React from 'react'

import './ParkMap.css'

// Represents a grid square with a color

function MapSquare(props) {
  const classes = `grid-square color-${props.color}`
  return <div className={classes} />
}

function MapGrid(props) {

  const parking = props.parkMap.split('\n')
  const grid = parking.map((row, r_idx) => (
    row.split('').map((spot, c_idx) => (
      <MapSquare key={`${c_idx}${r_idx}`} color={spot} />
    ))
  ))

  return (
    <div style={{
    display: 'grid',
    gridGap: 5,
    gridTemplateColumns: `repeat(${parking[0].length}, 20px)`,
    }}>
      {grid}
    </div>
  )
}

export default MapGrid;
