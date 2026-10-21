# R/grid drawing with the user's Snakemake diagram colours and layout
library(grid)
root <- if(exists('project_dir')) project_dir else getwd()
palette <- c(green='#59D856',cyan='#56D8D8',yellow='#D6D856',red='#D85656')

label <- function(text,x,y,size=12,bold=FALSE,just=c('centre','centre')) {
  grid.text(text,unit(x,'in'),unit(y,'in'),just=just,
    gp=gpar(fontfamily='Times',fontsize=size,
            fontface=if(bold) 'bold' else 'plain',col='black',lineheight=1.15))
}
node <- function(title,note,x,y,width,height,colour) {
  grid.roundrect(unit(x,'in'),unit(y,'in'),unit(width,'in'),unit(height,'in'),
    r=unit(.20,'in'),gp=gpar(fill='white',col=colour,lwd=2))
  label(title,x,y+.13,14,TRUE)
  label(note,x,y-.14,11)
}
edge <- function(x,y) {
  grid.lines(unit(x,'in'),unit(y,'in'),
    arrow=arrow(length=unit(.12,'in'),type='closed'),
    gp=gpar(col='black',fill='black',lwd=1.15))
}
infographic <- function() {
  grid.newpage()
  grid.rect(gp=gpar(fill='white',col=NA))
  label('18 October 2026',9.45,7.70,9,just=c('right','centre'))
  label('Potash fertilizer',5,7.57,22,TRUE)
  label('Potassium chloride (KCl) supplies potassium for crops',5,7.17,12)

  # Two real production routes meet at the finished fertilizer stage
  node('Potash deposit','KCl mixed with sodium chloride (NaCl)',
       5,6.37,4.55,.76,palette['green'])
  node('Underground mining','Cut and lift solid ore',
       2.23,5.13,2.95,.80,palette['cyan'])
  node('Solution mining','Pump in warm salty water',
       7.77,5.13,2.95,.80,palette['cyan'])
  node('Crush and separate','Recover KCl from the ore',
       2.23,3.87,2.95,.86,palette['yellow'])
  node('Cool the salty water','Collect the KCl crystals',
       7.77,3.87,2.95,.86,palette['yellow'])
  node('Dry and size','KCl fertilizer',
       5,2.73,2.50,.75,palette['red'])

  edge(c(3.78,2.23),c(5.99,5.55))
  edge(c(6.22,7.77),c(5.99,5.55))
  edge(c(2.23,2.23),c(4.71,4.32))
  edge(c(7.77,7.77),c(4.71,4.32))
  edge(c(2.74,4.42),c(3.42,3.12))
  edge(c(7.26,5.58),c(3.42,3.12))

  label(expression(KCl~'(s)' %->% K^'+'~'(aq)' + Cl^'-'~'(aq)'),
        .55,1.89,15,just=c('left','centre'))
  label('s = solid     aq = dissolved in water',.55,1.54,10,
        just=c('left','centre'))
  label('Cooling forms solid KCl again',.55,1.30,10,
        just=c('left','centre'))

  label('1964  Belle Plaine solution mine opens',5.55,1.96,10,
        just=c('left','centre'))
  label('Mines need water, energy and transport',5.55,1.69,10,
        just=c('left','centre'))
  label('Chemists test quality and improve separation',5.55,1.42,10,
        just=c('left','centre'))
  label('Mining jobs and salty waste to manage',5.55,1.15,10,
        just=c('left','centre'))

  label('(NRCan, 2026; Nutrien, n.d.; SMA, n.d.; Flowers et al., 2019)',5,.81,8)
  label('(Mosaic, n.d.; Kaiser & Rosen, 2018; Nutrien, 2026; Saskatchewan ER, 2023)',5,.61,8)
  label('Rayan Faisal',.55,.30,9,just=c('left','centre'))
  label('ORCID 0009-0005-1111-1501',5,.30,9)
  label('Made in R with Snakemake',9.45,.30,9,just=c('right','centre'))
}
if(!exists('load_only') || !isTRUE(load_only)) {
  pdf(file.path(root,'Potash_Infographic.pdf'),width=10,height=8,
      family='Times',useDingbats=FALSE,title='Potash fertilizer',author='Rayan Faisal')
  infographic();dev.off()
  png(file.path(root,'Potash_Infographic.png'),width=2500,height=2000,
      res=250,type='quartz',bg='white')
  infographic();dev.off()
  writeLines(c('Infographic drawn entirely in R/grid',paste('R version:',getRversion()),
               'Built through Snakemake','Outline colours sampled from the supplied Snakemake reference',
               paste(names(palette),palette)),file.path(root,'render_log.txt'))
}
