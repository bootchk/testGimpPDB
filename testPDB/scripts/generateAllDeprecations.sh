# generateAllDeprecations.#!/bin/sh

cat known.deprecations hidden.deprecations undocumentedDeprecations.data | sort | uniq > all.deprecations
gawk '{ print $1}' all.deprecations | uniq > allDeprecated
gawk '{ print $3}' all.deprecations | sort | uniq > allDeprecatees
