##### Signed by https://keybase.io/jdekker
```
-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1.4.11 (GNU/Linux)

iQIcBAABAgAGBQJTn3GgAAoJEJrQ9RIUCT6/CI4P/RSAQrd6JugGZoQu/gNdW6eB
MYCybqYGZiieVhUaGOnFNVlp68YpXH+sP/Uc6hXEX30UQEsDmhMeT5NA7ZMS+zJ9
MNHGQdJq22lGb3+VoVBV4RTMdkQXOXvx6p5biskjIEtM3tfTxP529GvAX2TFUNnt
gGWk28EDr30M95XwDxwWo+57Xv8VtSb3VSvXEbrdwGYf8EoQo9oPtzYQ0YcdupcC
ET8bukYVcwpAjoTnPlEy89TiHHohwmimr2ASXeQ64Ks5wfjzcF7NENCAmaAfR+KI
VLLuGqdWMBx1ewVuAXTCZ0Mga/kBoRUaO0PC13UmL8LhhZY9Z3cwD4UnPU35/RQi
IbLfQcZHf/gEvyMeiTYCsyWpm+/xxn1+EfHol4/Q9VSXzZgRBX05Ik6tqeCvjdgG
4PyHBaJTTm/HfMNdg3mr1mbyjTv5UxglEyPv+Y4NdfoVfepkXsXbzvNSyVffZ3Bw
UaFp7KzIC4Jugdpv63FleiAdDY0+iZ5shH86wD1+HJ0/a87kn5Ao1yESby7J7U+f
poZQYeMFeuC0T5hY/3iYoyvZ68oH918ESESiucSulp5BvfwuqGL2+xo5uJIwGYXE
3IDQC7xbA14JHX86IVJlSHAD33iWyiC+5yjw4/bRRVl37KPsLdHiXH3YIRnF5I2I
ZbM/uDYyJdZbBe4UoCoF
=AMhi
-----END PGP SIGNATURE-----

```

<!-- END SIGNATURES -->

### Begin signed statement 

#### Expect

```
size  exec  file                      contents                                                        
            ./                                                                                        
375           .gitignore              d2e475a6a4fa51422cac0a07495914e776858fb9ab9c8937a4d491a3e042d6b1
464           .travis.yml             3063ba078607b8d16bd6467afc15fbbaa4b26c1e30be5ce7cef453cfccbaa95c
428           Changelog.md            c7791d1914ddca9ff1549d90468a79787a7feafe94cecd756e3d7cbd4bcbc7df
              FourmiCrawler/                                                                          
0               __init__.py           e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
304             items.py              b00d49a3d53fa13306c7f8b023adb93ab88423c4fce46600689814f6b02bb806
2178            pipelines.py          f9b7b84938060751e15e45de5133dffe50c798bff2a20019206fe7c9d677ad49
914             settings.py           0be2eaf8e83e85ed27754c896421180fc80cb5ce44449aa9f1048e465d1a96f2
                sources/                                                                              
9991              ChemSpider.py       847013e34c5c3683ec66a337837287512b4bab9fbea2ece12e4130ab0dbf264d
9898              NIST.py             97abc84fce85c47b789822715a1945ab84cc052a32340c861141c1af66bab644
4754              PubChem.py          58ed4c92519e385f2768cf8034b006b18f8a21632cb1c5a0849b1a329a8c6ffb
6907              WikipediaParser.py  5d6de911c773129a34b76c40a9b547aafc67644a15f39cd0be6afc7a16fb0f97
0                 __init__.py         e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
1262              source.py           16c4cdfca849b7dc2bc89d7a6f7ad021f4aa1d04234394312f1d0edf0fd9c5a4
3026            spider.py             1ffba2512988b7a6b535a4a31a4ef688ece4f8c595c3d50355c34ef46b23e44a
1081          LICENSE                 36951e5f1910bad3e008ab7228f35ad8933192e52d3c3ae6a5e875765e27192c
3965          README.md               d21236d6a175be28ef8e2fee8a256e95b6a513163e3f1071c26c62e9093db7f3
3676  x       fourmi.py               2ff89f97fd2a49d08417d9ab6cf08e88944d0c45f54ec84550b530be48676c23
261           scrapy.cfg              624c068fd06303daa65b8e0d0d3ef88ac1f123be2694ef5b4f3f9a9dcd983f85
              tests/                                                                                  
1               __init__.py           01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b
2837            test_configurator.py  4a0eb6e7121eb09a63ab5cb797570d1a42080c5346c3b8b365da56eefa599e80
1892            test_pipeline.py      387a336b0f36722a20e712aa033e5771c44f9e92561dd73acffd53d622c52031
1260            test_sourceloader.py  b108b4b80adcdb7401273a9823b1f1a19eb5178776186eb5a9976aed8b1ee869
2113            test_spider.py        300f280377b522737be0d8e4a80031ab118a4011bdbb92131e9c400fcdab6299
              utils/                                                                                  
0               __init__.py           e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
3552            configurator.py       e2b7e0ee6c1fef4373785dfe5df8ec6950f31ce6a5d9632b69a66ea3d1eaf921
2537            sourceloader.py       f5a5ac2a6aba0658dbe11361f465caabcf3c06c5c8dc9a631874211cc19d2d37
```

#### Ignore

```
/SIGNED.md
```

#### Presets

```
git      # ignore .git and anything as described by .gitignore files
dropbox  # ignore .dropbox-cache and other Dropbox-related files    
kb       # ignore anything as described by .kbignore files          
```

<!-- summarize version = 0.0.9 -->

### End signed statement

<hr>

#### Notes

With keybase you can sign any directory's contents, whether it's a git repo,
source code distribution, or a personal documents folder. It aims to replace the drudgery of:

  1. comparing a zipped file to a detached statement
  2. downloading a public key
  3. confirming it is in fact the author's by reviewing public statements they've made, using it

All in one simple command:

```bash
keybase dir verify
```

There are lots of options, including assertions for automating your checks.

For more info, check out https://keybase.io/docs/command_line/code_signing