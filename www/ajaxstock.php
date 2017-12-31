<?php
  $sym = $_REQUEST["sym"];

  $lines = file('symbols.txt');
  $pattern=preg_quote($sym, '/');
  $pattern = "/^$pattern;/m";
  foreach($lines as $line) {
    if (preg_match($pattern, $line)) {  
      echo "<tr>";
      $values = explode(";", $line);
      foreach($values as $value) {
        echo "<td>" . $value . "</td>";
      }
      echo "</tr>";
    }
  }
?>
