# manage_pic
my graduated project 



思路: 添加用户操作记录日志
     超管审核的时候使用redis，redis存储的是固定数量的id   (useid  or menu_id ),每次审核取出redis的一个id  对对应的数据库做修改
     与客户端交互的时候 统一使用 json传递信息  (由于只需要交换菜式信息   统一格式：   id: ** , name：*** ,introduction:*** , pic：********    )   （优惠信息类似交换）
     用户token信息更改为使用redis
     需要使用redis的地方：1.用户token信息   2.用户审核   3.菜品审核

     前端界面使用 office_msg来实现



     客户端与服务器端沟通的方案 应该是？