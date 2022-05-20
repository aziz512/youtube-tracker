import { useEffect, useState } from 'react';
import styled from 'styled-components';
import DeleteButton from './DeleteButton';

const Home = () => {
  const [channels, setChannels] = useState([]);
  const [isSubscribed, setIsSubscribed] = useState();

  useEffect(() => {
    (async () => {
      const receivedChannels = await fetch('http://127.0.0.1:5000/videos').then(
        (res) => res.json()
      );
      setChannels(receivedChannels);
    })();
  }, [isSubscribed]);

  return (
    <>
      {channels.map(({ channel: { name, id }, videos }) => (
        <ChannelContainer key={id}>
          <Channel>
            <h3>{name}</h3>
            <DeleteButton
              name={name}
              id={id}
              isSubscribed={isSubscribed}
              setIsSubscribed={setIsSubscribed}
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
