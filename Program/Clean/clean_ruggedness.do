set more off
set matsize 10000


use "Data/Interim/geo_panel.dta", clear
duplicates drop OBJECTID, force
*Read raster files and save as dta
sum OBJECTID
local rows=r(N)
cd "Data/Raw/eleraster"
forvalues i=1/`rows'{
	local id=OBJECTID[`i']
	preserve
	ras2dta, files(elev`id') extension("txt") genxcoord(xid) genycoord(yid) clear replace
	restore
}
cd ../../..

set more off
use "Data/Interim/geo_panel.dta", clear
duplicates drop OBJECTID, force
sum OBJECTID
local rows=r(N)
matrix rgmat=(.,.)
forvalues i=1/`rows' {
	local id=OBJECTID[`i']
	scalar oid=`id'
	preserve
	use "Data/Raw/eleraster/elev`id'.dta", clear
	sum elev
	local N=r(N)
	sum xid
	local xnum=r(max)
	gen ruggedness=.
	forvalues j=1/`N' { 
		scalar tle=elev`id'[xid[`j']-1+`xnum'*(yid[`j']-1-1)]
		scalar tce=elev`id'[xid[`j']+`xnum'*(yid[`j']-1-1)]
		scalar tre=elev`id'[xid[`j']+1+`xnum'*(yid[`j']-1-1)]
		scalar cle=elev`id'[xid[`j']-1+`xnum'*(yid[`j']-1)]
		scalar cce=elev`id'[xid[`j']+`xnum'*(yid[`j']-1)]
		scalar cre=elev`id'[xid[`j']+1+`xnum'*(yid[`j']-1)]
		scalar ble=elev`id'[xid[`j']-1+`xnum'*(yid[`j']+1-1)]
		scalar bce=elev`id'[xid[`j']+`xnum'*(yid[`j']+1-1)]
		scalar bre=elev`id'[xid[`j']+1+`xnum'*(yid[`j']+1-1)]
		disp tle tce tre cle cce cre ble bce bre
		foreach adgrid in tle tce tre cle cce cre ble bce bre{
			if `adgrid'==. scalar `adgrid'=cce
		}
		replace ruggedness=((tle-cce)^2+(tce-cce)^2+(tre-cce)^2+(cle-cce)^2+(cre-cce)^2+(ble-cce)^2+(bce-cce)^2+(bre-cce)^2)^0.5 in `j' 
	}
	sum ruggedness
	matrix rgmat=(rgmat\oid, r(mean))
	restore
}

*matrix list rgmat
clear
svmat rgmat, names(v)
drop in 1
rename v1 OBJECTID
rename v2 ruggedness
label variable ruggedness "Ruggedness Index"
save "Data/Interim/ruggedness.dta", replace