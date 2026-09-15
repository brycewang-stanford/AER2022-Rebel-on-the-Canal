set more off
set matsize 10000


import delimited using "Data/Raw/Mann/allproxyfieldrecon.csv", delimiter(" ", collapse) clear 
save "Data/Interim/mann_raw.dta", replace

import delimited "Data/Raw/Mann/longlat.csv", delimiter(" ", collapse) clear 
rename v2 lon
rename v3 lat
gen cellid=_n
keep cellid lon lat
save "Data/Interim/mann_loc.dta", replace

use "Data/Interim/mann_raw.dta", clear
drop v1
rename v2 year
stack v3-v2594, into(recon) clear
rename _stack cellid
gen i=_n
sort cellid
by cellid: gen year=_n+499
keep cellid recon year
save "Data/Interim/mann_xt.dta", replace

use "Data/Interim/mann_loc.dta", clear
keep if lon>=100 & lon<=130 & lat>=20 & lat<=50
gen mid=_n
expand 575
sort mid
by mid: gen _ID=_n
merge m:1 _ID using "Data/Interim/samplemap_d.dta"
keep lon lat cellid OBJECTID _ID X_COORD Y_COORD
geodist lat lon Y_COORD X_COORD, gen(dist)
sort _ID
by _ID: egen dmin=min(dist)
gen dg=dist-dmin
keep if dg<0.01
by _ID: gen alt=_n
expand 2006-500+1
sort _ID alt
by _ID alt: gen year=_n+499
merge m:1 cellid year using "Data/Interim/mann_xt.dta"
keep if _merge==3
drop _merge
collapse (mean) OBJECTID cellid recon (count) alt, by(_ID year)
keep if year>=1650 & year<=1911
keep OBJECTID year recon cellid
label variable recon "Temperature Deviated from 1961-2006 Mean"
label variable cellid "ID of the Reconstructed Cell of Temperature"
save "Data/Interim/mann_recon.dta", replace