3 co-ordinates per iteration. End is averaged out
<ol>
  <li>Substitue X in. </li>
  <li>Subtract c from first two equations to be left with ax^2 + bx = y</li>
  <li>Factorise out na + b = k where n and k are variables</li>
  <li>Repeate the same steps with equations 2 & 3 instead of 1 & 2</li>
  <li>Subtract out b from two resultanmts</li>
  <li>Substitute new found value for a into first equation to calculate b</li>
  <li>Substitue a & b into fiest equation to calculate c</li>
  <li> Return all values</li>
<ol>
  
<h3>General example</h3>
<h5>Initial equations</h5>
<ul>
<li>aX[0]^2 + bX[0] + c = Y[0]</li>
<li>aX[1]^2 + bX[1] + c = Y[1]</li>
<li>aX[2]^2 + bX[2] + c = Y[2]</li>
</ul>
<p><i> Where X and Y are inputs provided by the user</i></p>

<h3> Subtraction results</h3>
<p><b>Equations 1 & 2</b></p>
a(X[0] + X[1]) + b = (Y[0] - Y[1]) / (X[0] - X[1])

<p><b>Equations 2 & 3</b></p>
a(X[1] + X[2]) + b = (Y[1] - Y[2]) / (X[1] - X[2])

<p><b>Subntraction of the two results</b></p>
a(X[0] - X[2]) = ((Y[0] - Y[1]) / (X[0] - X[1])) - ((Y[1] - Y[2]) / (X[1] - X[2]))
  </br>




