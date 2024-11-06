# ComfyUI_Demucs  
Using [Demucs](https://github.com/facebookresearch/demucs) in comfyUI     
Demucs 音频分离开源方法在comfyUI这个GUI上的简单实现； 

----

**TIPS:
* using workflow in dir,no need any models./简单用不需要模型；  
* mixed=bass+drums+other,input audio=bass+drums+other+vocal/合成好的分离音频是mixed（=bass+drums+other），人声是vocal；  

1.Installation  
-----
  In the ./ComfyUI /custom_node directory, run the following:   
```
git clone https://github.com/smthemex/ComfyUI_Demucs.git
```
2.requirements  
----

```
pip install -r requirements.txt 
```

3.Example
----   

![](https://github.com/smthemex/ComfyUI_Demucs/blob/main/example.png)


4.Citation
------

**facebookresearch/demucs**
``` python  
@inproceedings{rouard2022hybrid,
  title={Hybrid Transformers for Music Source Separation},
  author={Rouard, Simon and Massa, Francisco and D{\'e}fossez, Alexandre},
  booktitle={ICASSP 23},
  year={2023}
}

@inproceedings{defossez2021hybrid,
  title={Hybrid Spectrogram and Waveform Source Separation},
  author={D{\'e}fossez, Alexandre},
  booktitle={Proceedings of the ISMIR 2021 Workshop on Music Source Separation},
  year={2021}
}
}```
