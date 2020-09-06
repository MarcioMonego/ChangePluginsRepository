## **This plugin changes the Git repository/plugins file for your Craftbeerpi plugins to one you choose**

This plugin allows you to change the original Git repository where Craftbeerpi finds the plugins list.   
This way you can clone original Crafbeerpi plugins repository(https://github.com/Manuel83/craftbeerpi-plugins.git) to use you own repository or another.

### **To change the plugin list to a repository of your choice:**

* On your Craftbeerpi installation folder on Raspberry pi 

* Create a folder for this plugin with the name of ChangePluginsRepository(maintaining ths same avoids duplication if this merge with the original Craftbeerpi)

* Do a Git clone of this repository with the command Git clone https://github.com/marciomonego/ChangePluginsRepository.git

* Reestart your Craftbeerpi!

Now there will be a system parameter to define your plugins repository and the default value will be the original Craftbeerpi one.   

**Note:**   
The final url used points directly to plugins.yaml and not to the repository root!    

Same way the url to make the request without errors is like the original one used by Craftbeerpi, like:
https://raw.githubusercontent.com/GitHubeAccount/craftbeerpi-plugins/master/plugins.yaml, and this will be the default value after install the plugin to avoid user mistakes like just download the plugin and never configure it.

If you want, change the original Craftbeerpi repository to a repository or a fork you made/choose or another one just replace the parameter `Plugins_Repository` under Craftbeerpi system parameters.
It will be with default value since the plugin installation to guide you.

### **Very important!**

If you want to never loose a new plugin added to the original Crafbeerpi repository then the better choice is to `merge` original Crafbeerpi with you fork or another repository, then you can set the new parameter `Plugins_Repository_MergeWithOriginal` with `Yes` value!
If you define it to Yes then this plugin will merge all of original plugins list in the Craftbeerpi repository with the new records of you repository, this way your repository of plugins NEED only plugins not accepted/intregrated by Manuel and not all like when you fork the orignal one.

### **Disclaimer**

This plugin doesn't is concerned to replace original Craftbeerpi one, it was just concerned to cut the time needed beetween the release of community plugin and the acception by Manuel to new plugins.
As the plugins are integrated to original repository you can delete the records of you own and stay with the defined on original repository.
