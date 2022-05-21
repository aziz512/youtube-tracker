import { useEffect, useState } from 'react';
import styled from 'styled-components';
import { HOST } from '../common';
import AddChannel from './AddChannel';
import DeleteButton from './DeleteButton';

const Home = () => {
  let [channels, setChannels] = useState([]);
  const [isSubscribed, setIsSubscribed] = useState();

  useEffect(() => {
    (async () => {
      const receivedChannels = await fetch(`${HOST}/videos`).then((res) =>
        res.json()
      );
      setChannels(receivedChannels);
    })();
  }, [isSubscribed]);

  const onChannelAdded = (channelData) => {
    // avoid adding undefined values and duplicates
    if (
      channelData &&
      !channels.some(({ channel: { id } }) => id === channelData.channel.id)
    ) {
      setChannels([...channels, channelData]);
    }
  };

  const handleDeleteRequest = async (id) => {
    try {
      const resp = await fetch(`${HOST}/watchlist`, {
        method: 'DELETE',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id }),
      });
      if (resp.ok) {
        removeChannel(id);
        setIsSubscribed(!isSubscribed);
        console.log('running');
      }
    } catch (e) {
      console.log(e, 'Failed to delete channel');
    }
  };

  const removeChannel = (channelId) => {
    channels = channels.filter((element) => {
      return element.id !== channelId;
    });
  };

  return (
    <>
      <AddChannel onChannelAdded={onChannelAdded} />

      {channels.map(({ channel: { name, id }, videos }) => (
        <ChannelContainer key={id}>
          <Channel>
            <h3>{name}</h3>
            <DeleteButton
              handleDeleteRequest={() => {
                handleDeleteRequest(id);
              }}
            />
          </Channel>
          <VideosContainer>
            {videos.map((video) => (
              <VideoItem key={video.id}>
                <LinkWrapper
                  href={'https://www.youtube.com/watch?v=' + video.id}
                  target="_blank"
                >
                  <Thumbnail src={video.thumbnail} />
                  <span>{video.title}</span>
                </LinkWrapper>
              </VideoItem>
            ))}
          </VideosContainer>
        </ChannelContainer>
      ))}
    </>
  );
};

export default Home;

const ChannelContainer = styled.div`
  // padding-top: 30px;
  padding: 10px;
`;

const VideosContainer = styled.div`
  width: 100%;
  overflow-x: auto;
  white-space: nowrap;
  overflow-y: hidden;
`;

const VideoItem = styled.div`
  display: inline-block;
  vertical-align: top;
  white-space: break-spaces;
  margin: 0 10px 0 0;
  width: 220px;
`;

const Thumbnail = styled.img`
  width: 100%;
  display: block;
`;

const LinkWrapper = styled.a`
  &:any-link {
    color: black;
    text-decoration: none;
  }
`;

const Channel = styled.div`
  display: flex;
  align-content: center;
  justify-content: flex-start;
  align-items: center;
`;
